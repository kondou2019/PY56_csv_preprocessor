#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Optional

import click

from src.csv import csv_file_reader, csv_file_writer
from src.table_utl import (
    CsvReportInfo,
    column_exclusive_index_group,
    column_fill_index,
    column_merge_index_group,
    csv_filetype_detect,
    csv_filetype_list_read,
    csv_filetype_read,
    table_report,
    table_sort,
)


def option_path(input: Optional[str], output: Optional[str]) -> tuple[Optional[Path], Optional[Path]]:
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


def option_value_list(value_list: str) -> list[str]:
    """!
    @brief オプションのリスト指定の共通処理を行う
    @param value_list 値リスト,"[value[,...]]"
    @return インデックスリスト
    """
    return [v for v in value_list[1:-1].split(",")]


def custom_group_index_list(ctx: click.core.Context, param: click.Option, value: tuple[str, ...]):
    """!
    @brief 独自のチェックを行う関数。グループインデックスリストのチェックを行う。
    """
    for v in value:
        if v[0] != "[" or v[-1] != "]":
            raise click.BadParameter('インデックスリストは"[index[,...]]"の形式である必要があります。')
    return value


def custom_index_list(ctx: click.core.Context, param: click.Option, value: str):
    """!
    @brief 独自のチェックを行う関数。インデックスリストのチェックを行う。
    """
    if value[0] != "[" or value[-1] != "]":
        raise click.BadParameter('インデックスリストは"[index[,...]]"の形式である必要があります。')
    return value


def custom_value_list(ctx: click.core.Context, param: click.Option, value: Optional[str]):
    """!
    @brief 独自のチェックを行う関数。リスト形式の値のチェックを行う。
    @details 値は文字列を想定している。
    """
    if value is None:
        return value
    if value[0] != "[" or value[-1] != "]":
        raise click.BadParameter('リストは"[value[,...]]"の形式である必要があります。')
    return value


@click.command(help="カラムを追加")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", type=int, required=True, help="追加するカラム(インデックス)。インデックスの前に追加する。最後に追加する場合は、-1を指定する。")
def column_add(input: Optional[str], output: Optional[str], column: int) -> int:
    """!
    @brief カラムを追加
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.table_column_add(column)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", type=int, required=True, help="削除するカラム(インデックス)")
def column_del(input: Optional[str], output: Optional[str], column: int) -> int:
    """!
    @brief カラムを削除
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.table_column_del(column)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムを排他。--column-groupで指定したカラムグループを別々の行に分離する")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column-group",
    callback=custom_group_index_list,
    multiple=True,
    required=True,
    type=str,
    help="カラムのインデックスリスト。2回以上指定する。[index[,...]]",
)
@click.option("--header", type=int, default=0, show_default=True, help="ヘッダの行数。ヘッダは処理の対象になりません")
def column_exclusive(input: Optional[str], output: Optional[str], column_group: tuple[str], header: int) -> int:
    """!
    @brief カラムを排他
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


@click.command(help="カラムの欠損値を置換(穴埋め)")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", type=int, required=True, help="対象のカラム(インデックス)")
@click.option("--value", type=str, default="", show_default=True, help="置換する値")
@click.option("--ffill", is_flag=True, help="前の行からの穴埋め")
def column_fill(input: Optional[str], output: Optional[str], column: int, value: str, ffill: bool) -> int:
    """!
    @brief カラムの欠損値を置換(穴埋め)
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    column_fill_index(tbl, column, value, ffill=ffill)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムをマージ。column-exclusiveで排他した行をマージして元にもどす")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column-key",
    callback=custom_index_list,
    required=True,
    type=str,
    help="マージする行で一致するカラム。[index[,...]]",
)
@click.option(
    "--column-group",
    callback=custom_group_index_list,
    multiple=True,
    required=True,
    type=str,
    help="カラムのインデックスリスト。2回以上指定する。[index[,...]]",
)
@click.option("--header", type=int, default=0, show_default=True, help="ヘッダの行数。ヘッダは処理の対象になりません")
def column_merge(
    input: Optional[str], output: Optional[str], column_key: str, column_group: tuple[str, ...], header: int
) -> int:
    """!
    @brief カラムを排他
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_key_index_list = option_index_list(column_key)
    column_group_list = [option_index_list(i) for i in column_group]
    # 実行
    tbl = csv_file_reader(input_path, header=header)
    column_merge_index_group(tbl, column_key_index_list, column_group_list)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムを移動")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--from", "from_", type=int, required=True, help="移動元のカラム(インデックス)")
@click.option("--to", type=int, required=True, help="移動先のカラム(インデックス)")
def column_move(from_: int, to: int, input: Optional[str], output: Optional[str]) -> int:
    """!
    @brief カラムを移動
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.column_move(from_index=from_, to_index=to)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="カラムを選択")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--start", type=int, required=True, help="開始のカラム(インデックス)")
@click.option("--end", type=int, required=True, help="終了のカラム(インデックス)")
def column_select(start: int, end: int, input: Optional[str], output: Optional[str]) -> int:
    """!
    @brief カラムを選択
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    new_tbl = tbl.table_select_column_range(start_index=start, end_index=end + 1)
    csv_file_writer(output_path, new_tbl)
    return 0


@click.command(help="カラムでソート")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column-key",
    callback=custom_index_list,
    required=True,
    type=str,
    help="ソートするカラムのインデックスリスト。[index[,...]]",
)
@click.option(
    "--column-attr",
    callback=custom_value_list,
    type=str,
    help="ソートするカラムの属性(str,int,float)。省略時はすべてstr。[attr[,...]]",
)
@click.option("--header", type=int, default=0, show_default=True, help="ヘッダの行数。ヘッダは処理の対象になりません")
@click.option("--reverse", is_flag=True, help="降順にソート")
def column_sort(
    input: Optional[str], output: Optional[str], column_key: str, column_attr: Optional[str], header: int, reverse: bool
) -> int:
    """!
    @brief カラムでソート
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_key_index_list = option_index_list(column_key)
    if column_attr is None:
        column_attr_list = ["str"] * len(column_key_index_list)
    else:
        column_attr_list = option_value_list(column_attr)
    # 実行
    tbl = csv_file_reader(input_path, header=header)
    table_sort(tbl, set(column_key_index_list), column_attr_list, reverse=reverse)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="CSVファイルの種別を判定")
@click.option("--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def csv_filetype(csv_info_dir: str, files: tuple[str, ...]) -> int:
    """!
    @brief CSVファイルの種別を判定する
    @retval 0 正常終了
    @retval 1 異常終了
    """
    csv_info_dir_path = Path(csv_info_dir)
    # CSV種別のリストを作成
    csv_type_list = csv_filetype_list_read(csv_info_dir_path)
    if len(csv_type_list) == 0:
        print("CSV情報ファイルが見つかりません。", file=sys.stderr)
        return 1
    # ファイルの種別判定
    for file in files:
        file_path = Path(file)
        #
        csv_type = csv_filetype_detect(csv_type_list, file_path)
        if csv_type is not None:
            print(f"{file}\t{csv_type.type_name}")
        else:
            print(f"{file}\t***unknown***")
    return 0


@click.command(help="CSVファイルにヘッダを追加")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--add-header", type=click.Path(exists=True), required=True, help="追加するCSVヘッダファイル")
def csv_header_add(input: Optional[str], output: Optional[str], add_header: str) -> int:
    """!
    @brief CSVファイルにヘッダを追加
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    add_header_path = Path(add_header)
    # 実行
    add_csv_filetype = csv_filetype_read(add_header_path)  # 追加するCSVヘッダファイルを読み込む
    tbl = csv_file_reader(input_path)
    tbl.table_header_add(add_csv_filetype)
    csv_file_writer(output_path, tbl)

    return 0


@click.command(help="CSVファイルのヘッダを変更")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--input-header", type=click.Path(exists=True), required=True, help="変更前CSVヘッダファイル")
@click.option("--output-header", type=click.Path(exists=True), required=True, help="変更後CSVヘッダファイル")
def csv_header_change(input: Optional[str], output: Optional[str], input_header: str, output_header) -> int:
    """!
    @brief CSVファイルのヘッダを変更する
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # CSVヘッダファイルの種別を読み込む
    input_csv_filetype = csv_filetype_read(Path(input_header))
    output_csv_filetype = csv_filetype_read(Path(output_header))
    # 実行
    tbl = csv_file_reader(input_path, csv_filetype=input_csv_filetype)
    tbl.table_header_del()  # ヘッダを削除
    tbl.table_header_add(output_csv_filetype)  # 新しいヘッダを追加
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="CSVファイルのヘッダを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--header", type=int, required=True, help="ヘッダの行数")
def csv_header_del(input: Optional[str], output: Optional[str], header: int) -> int:
    """!
    @brief CSVファイルのヘッダを削除
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.table_header_del(header_count=header)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(help="CSVファイルの情報を表示")
@click.option("--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def csv_report(csv_info_dir: str, files: tuple[str, ...]) -> int:
    """!
    @brief CSVファイルの情報を表示する
    @retval 0 正常終了
    @retval 1 異常終了
    """
    csv_info_dir_path = Path(csv_info_dir)
    # CSV種別のリストを作成
    csv_type_list = csv_filetype_list_read(csv_info_dir_path)
    if len(csv_type_list) == 0:
        print("CSV情報ファイルが見つかりません。", file=sys.stderr)
        return 1
    # ファイルのレポートを作成
    csv_report_info_list: list[CsvReportInfo] = []
    for file in files:
        file_path = Path(file)
        #
        report_info = table_report(csv_type_list, file_path)
        csv_report_info_list.append(report_info)
    # ファイルの情報をJSON形式で表示
    print(json.dumps([x.__dict__ for x in csv_report_info_list], indent=2))
    return 0


# サブコマンドをメインコマンドに追加
@click.group(help="CSVファイルの前処理ツール")
@click.version_option()
def cli():
    pass


cli.add_command(column_add)
cli.add_command(column_del)
cli.add_command(column_exclusive)
cli.add_command(column_fill)
cli.add_command(column_merge)
cli.add_command(column_move)
cli.add_command(column_select)
cli.add_command(column_sort)
cli.add_command(csv_filetype)
cli.add_command(csv_header_add)
cli.add_command(csv_header_change)
cli.add_command(csv_header_del)
cli.add_command(csv_report)

if __name__ == "__main__":
    rc = cli(standalone_mode=False)
    sys.exit(rc)
