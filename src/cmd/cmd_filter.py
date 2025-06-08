import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Optional

import click

from src.cmd.cmd_common import option_path
from src.filter.filter_base import FilterBase
from src.lib.csv import csv_file_reader, csv_file_writer
from src.lib.table_utl import CsvFileTypeInfo, csv_filetype_read


def dynamic_import(module_name, module_path):
    """
    指定されたパスからモジュールを動的にインポートする関数
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@click.command(name="filter", help="フィルター。フィルターモジュールによる加工")
@click.option("--filter-name", type=str, required=True, help="フィルター名称")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
def cmd_filter(
    filter_name: str,
    input: Optional[str],
    output: Optional[str],
) -> None:
    input_path, output_path = option_path(input, output)
    # 実行
    ## csvデータ入力
    tbl = csv_file_reader(input_path)
    ## filter加工
    ### filter モジュールの取得
    #### 動的にpythomモジュールをimport
    project_dir = Path(__file__).parent.parent
    filter_dir = project_dir.joinpath("filter")
    filter_path = filter_dir.joinpath(filter_name).joinpath("filter.py")
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
    filter_obj = filter_class.new_filter()
    tbl_new = filter_obj.filter_execute(tbl)
    ## csvデータ出力
    ### 出力
    csv_file_writer(output_path, tbl_new)
    return
