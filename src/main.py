#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Optional

import click

from src.csv import csv_file_reader, csv_file_writer
from src.table_utl import column_exclusive_index_group


def option_path(input: Optional[str], output: Optional[str]) -> (Optional[Path], Optional[Path]):
    """!
    @brief オプションのパスの共通処理を行う
    @param input 入力ファイル
    @param output 出力ファイル
    @return 入力ファイルと出力ファイルのパス
    """
    input_path: Optional[Path] = None
    if input is not None:
        input_path = Path(input)
    output_path: Optional[Path] = None
    if output is not None:
        output_path = Path(output)
    return (input_path, output_path)


def option_index_list(index_list: str) -> list[int]:
    """!
    @brief オプションのインデックスリストの共通処理を行う
    @param index_list インデックスリスト,"[index[,...]]"
    @return インデックスリスト
    """
    return [int(i) for i in index_list[1:-1].split(",")]


def custom_index_list(ctx: click.core.Context, param: click.Option, value: tuple[str]):
    """!
    @brief 独自のチェックを行う関数。インデックスリストのチェックを行う。
    """
    for v in value:
        if v[0] != "[" or v[-1] != "]":
            raise click.BadParameter('インデックスリストは"[index[,...]]"の形式である必要があります。')
    return value


@click.command(help="カラムの排他。--column-groupで指定したカラムグループを別々の行に分離する")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column-group",
    callback=custom_index_list,
    multiple=True,
    required=True,
    type=str,
    help="カラムのインデックスリスト。2回以上指定する。[index[,...]]",
)
@click.option("--header", type=int, default=0, show_default=True, help="ヘッダの行数,ヘッダ行は排他の対象になりません")
def column_exclusive(input: Optional[str], output: Optional[str], column_group: tuple[str], header: int) -> int:
    """!
    @brief カラムの排他
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_group_list = [option_index_list(i) for i in column_group]
    # 実行
    tbl = csv_file_reader(input_path, header=header)
    column_exclusive_index_group(tbl, column_group_list)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムの移動")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--from", "from_", type=int, required=True, help="移動元のカラム(インデックス)")
@click.option("--to", type=int, required=True, help="移動先のカラム(インデックス)")
def column_move(from_: int, to: int, input: Optional[str], output: Optional[str]) -> int:
    """!
    @brief カラムの移動
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.column_move(from_index=from_, to_index=to)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムの選択")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--start", type=int, required=True, help="開始のカラム(インデックス)")
@click.option("--end", type=int, required=True, help="終了のカラム(インデックス)")
def column_select(start: int, end: int, input: Optional[str], output: Optional[str]) -> int:
    """!
    @brief カラムの選択
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    new_tbl = tbl.table_select_column_range(start_index=start, end_index=end + 1)
    csv_file_writer(output_path, new_tbl)
    return 0


@click.command(help="CSVファイルの種別を判定する")
@click.option("--header-dir", "-i", type=click.Path(exists=True), required=True, help="CSVヘッダファイルディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def csv_filetype(header_dir: str, files: tuple[str]) -> int:
    """!
    @brief CSVファイルの種別を判定する
    @retval 0 正常終了
    @retval 1 異常終了
    """
    header_dir_path = Path(header_dir)
    # CSV種別のリストを作成
    csv_type_list: list[tuple[str, list[str]]] = []  # (種別名, ヘッダ行のリスト)
    for file_path in header_dir_path.glob("*.csv"):
        with open(file_path, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
        #
        csv_type_list.append((file_path.stem, lines))
    # CSV種別のリストをヘッダ行の長い順にソート※1行目が同一の場合に間違って判定しないようにするため
    csv_type_list.sort(key=lambda x: len(x[1]), reverse=True)
    header_max_line = len(csv_type_list[0][1])
    # ファイルの種別判定
    for file in files:
        # ファイルの読み込み
        lines: list[str] = []
        with open(file, mode="r", encoding="utf-8") as f:
            for _ in range(header_max_line):  # header_max_line以上は読まない
                lines.append(f.readline())
        # ファイルの種別判定
        for key, value in csv_type_list:
            if lines[0 : len(value)] == value:
                print(f"{file}\t{key}")
                break
        else:
            print(f"{file}\t***unknown***")
    return 0


# サブコマンドをメインコマンドに追加
@click.group(help="CSVファイルの前処理ツール")
@click.version_option()
def cli():
    pass


cli.add_command(column_exclusive)
cli.add_command(column_move)
cli.add_command(column_select)
cli.add_command(csv_filetype)

if __name__ == "__main__":
    rc = cli(standalone_mode=False)
    sys.exit(rc)
