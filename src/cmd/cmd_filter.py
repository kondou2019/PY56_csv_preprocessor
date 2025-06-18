import glob
import importlib.util
import inspect
import os
import shlex
import sys
from pathlib import Path
from typing import Iterator, Optional

import click

from src.cmd.cmd_common import custom_index_list, option_index_list, option_path
from src.filter.filter_base import FilterBase, FilterType
from src.lib.csv import csv_file_reader, csv_file_writer


def dynamic_import(module_name, module_path):
    """
    指定されたパスからモジュールを動的にインポートする関数
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def parse_extra_args(args: list[str]) -> dict[str, Optional[str]]:
    """
    --key value、--key=value、--flag の形式を辞書に変換する。

    - --key value     → {"key": "value"}
    - --key=value     → {"key": "value"}
    - --flag（値なし）→ {"flag": None}

    :param args: -- 以降の引数リスト
    :return: 辞書形式に変換されたオプション
    :raises click.UsageError: 不正な形式の場合
    """
    result: dict[str, Optional[str]] = {}
    it = iter(args)

    for arg in it:
        if not arg.startswith("--"):
            raise click.UsageError(f"Invalid argument format: {arg}")

        key = arg[2:]
        if "=" in key:
            key, value = key.split("=", 1)
            result[key] = value
        else:
            # peek the next argument
            try:
                next_arg = next(it)
                if next_arg.startswith("--"):
                    # 次もオプションなら、これはフラグ扱い
                    result[key] = None
                    # 次のオプションをループで再処理するため戻す
                    it = _putback(it, next_arg)
                else:
                    result[key] = next_arg
            except StopIteration:
                # 最後が --flag のような形ならフラグ扱い
                result[key] = None

    return result


def _putback(iterator: Iterator, value: str) -> Iterator:
    """
    イテレータの先頭に値を戻す簡易ユーティリティ。
    """
    return iter([value] + list(iterator))


@click.command(name="filter", help="フィルター。フィルターモジュールによる加工")
@click.option("--filter-name", type=str, required=True, help="フィルター名称")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, type=str, help="カラムのインデックスリスト。[index[,...]]")
@click.option("--filter-option", type=str, help="フィルターオプション")
def cmd_filter(
    filter_name: str,
    input: Optional[str],
    output: Optional[str],
    column: Optional[str],
    filter_option: Optional[str],
) -> None:
    # オプション解析
    input_path, output_path = option_path(input, output)
    column_index_list: Optional[list[int]] = None
    if column is not None:
        column_index_list = option_index_list(column)
    ## フィルターのオプション
    filter_option_args: list[str] = []
    if filter_option is not None:
        filter_option_args = shlex.split(filter_option)
    else:
        filter_option_args = []
    # 実行
    ## csvデータ入力
    tbl = csv_file_reader(input_path)
    ## filter加工
    ### filter モジュールの取得
    #### 動的にpythomモジュールをimport
    project_dir = Path(__file__).parent.parent
    filter_dir = project_dir.joinpath("filter")
    filter_path = filter_dir.joinpath(filter_name.replace("-", "_")).joinpath("filter.py")
    if Path.is_file(filter_path) == False:
        raise click.ClickException("--filter-name で指定したフィルターが見つかりません。")
    filter_module = dynamic_import("filter_module01", filter_path)
    #### モジュール内のFilterBaseクラスを継承したクラスを取得
    filter_class = None
    class_list = [
        member
        for _name, member in inspect.getmembers(filter_module)
        if inspect.isclass(member) and member.__module__ == filter_module.__name__
    ]  # モジュールからクラスオブジェクトの一覧を作成
    for c in class_list:
        if issubclass(c, FilterBase):
            filter_class = c
            break
    else:
        raise click.ClickException("--filter-name で指定したフィルターの内容が不正です。")
    ### filter 実行
    filter_type = filter_class.filter_get_type()
    filter_obj = filter_class.new_filter(filter_option_args)
    if filter_type == FilterType.TABLE:
        tbl_new = filter_obj.filter_execute_table(tbl, column_index_list=column_index_list)
    elif filter_type == FilterType.COLUMNS:
        raise NotImplementedError()
    elif filter_type == FilterType.ROWS:
        raise NotImplementedError()
    elif filter_type == FilterType.CELL:
        if column_index_list is None:
            column_index_list = list(range(tbl.column_count()))
        #
        for row in tbl._rows:
            for index in column_index_list:
                cell = row[index]
                cell_new = filter_obj.filter_execute_cell(cell)
                row[index] = cell_new
        tbl_new = tbl

    # csvデータ出力
    csv_file_writer(output_path, tbl_new)
    return


@click.command(name="filter-list", help="フィルター一覧")
def cmd_filter_list() -> None:
    project_dir = Path(__file__).parent.parent
    filter_base = project_dir.joinpath("filter")
    for filter_dir in sorted(list(glob.glob(os.path.join(filter_base, "*")))):
        if os.path.isdir(filter_dir) == False:
            continue
        filter_path = os.path.join(filter_dir, "filter.py")
        if os.path.exists(filter_path) == False:
            continue
        filter_name = os.path.basename(filter_dir)
        filter_name = filter_name.replace("_", "-")
        print(filter_name)
