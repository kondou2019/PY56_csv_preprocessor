#!/usr/bin/env python3
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click

from src.csv import csv_file_reader, csv_file_writer
from src.table_utl import (
    CsvReportInfo,
    column_exclusive_index_group,
    column_fill_index,
    column_merge_index_group,
    column_quote,
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


@click.command(name="column-add", help="カラムを追加")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column",
    callback=custom_index_list,
    required=True,
    type=str,
    help="追加するカラムのインデックスリスト。インデックスの前に追加する。最後に追加する場合は、-1を指定する。[index[,...]]",
)
@click.option("--column-count", type=int, default=1, show_default=True, help="追加するカラム数")
def cmd_column_add(input: Optional[str], output: Optional[str], column: str, column_count: int) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in sorted(column_index_list, reverse=True):  # カラムの最後から追加する
        tbl.table_column_add(column, column_count=column_count)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="column-del", help="カラムを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="削除するカラムのインデックスリスト。[index[,...]]")
def cmd_column_del(input: Optional[str], output: Optional[str], column: str) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in sorted(column_index_list, reverse=True):  # インデックスの大きい順に削除する
        tbl.table_column_del(column)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="column-exclusive", help="カラムを排他。--column-groupで指定したカラムグループを別々の行に分離する")
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
def cmd_column_exclusive(input: Optional[str], output: Optional[str], column_group: tuple[str], header: int) -> int:
    """!
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


@click.command(name="column-fill", help="カラムの欠損値を置換(穴埋め)")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="対象のカラムのインデックスリスト。[index[,...]]")
@click.option("--value", type=str, default="", show_default=True, help="置換する値")
@click.option("--ffill", is_flag=True, help="前の行からの穴埋め")
def cmd_column_fill(input: Optional[str], output: Optional[str], column: str, value: str, ffill: bool) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in column_index_list:
        column_fill_index(tbl, column, value, ffill=ffill)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="column-merge", help="カラムをマージ。column-exclusiveで排他した行をマージして元にもどす")
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
def cmd_column_merge(
    input: Optional[str], output: Optional[str], column_key: str, column_group: tuple[str, ...], header: int
) -> int:
    """!
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


@dataclass
class ColumnMoveFromTo:
    index: int  # --fromオプションの順番
    from_: int
    to: int
    column_list: list[str]


@click.command(name="column-move", help="カラムを移動")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--from", "from_", callback=custom_index_list, required=True, type=str, help="移動元のカラムのインデックスリスト。[index[,...]]"
)
@click.option(
    "--to",
    callback=custom_index_list,
    required=True,
    type=str,
    help="移動先のカラムのインデックスリスト。--fromで削除された後のインデックスを指定する。[index[,...]]",
)
def cmd_column_move(from_: str, to: str, input: Optional[str], output: Optional[str]) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    from_column_index_list = option_index_list(from_)
    to_column_index_list = option_index_list(to)
    if len(from_column_index_list) != len(to_column_index_list):
        print("--fromと--toに指定したインデックスの数が一致しません。", file=sys.stderr)
        return 1
    #
    column_move_from_to: list[ColumnMoveFromTo] = []
    for i in range(len(from_column_index_list)):
        from_index = from_column_index_list[i]
        to_index = to_column_index_list[i]
        ft = ColumnMoveFromTo(index=i, from_=from_index, to=to_index, column_list=[])
        column_move_from_to.append(ft)
    # 実行
    tbl = csv_file_reader(input_path)
    # tbl.column_move(from_index=from_, to_index=to)
    ## 削除
    for ft in sorted(column_move_from_to, key=lambda x: x.from_, reverse=True):  # インデックスの大きい順に削除する
        column_list = tbl.column_remove(ft.from_)
        ft.column_list = column_list
    ## 追加;インデックスの大きい方から追加する。インデックスが同じ場合は--fromの順番を維持する
    for ft in sorted(column_move_from_to, key=lambda x: (x.to, x.index), reverse=True):
        tbl.column_insert(ft.to, ft.column_list)

    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="column-quote", help="カラムの値をクォートで囲む")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="カラムのインデックスリスト。[index[,...]]")
@click.option("--header", type=int, default=0, show_default=True, help="ヘッダの行数。ヘッダは処理の対象になりません")
def cmd_column_quote(input: Optional[str], output: Optional[str], column: str, header: int) -> int:
    """!
    @brief カラムの値をクォートで囲む
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path, header=header)
    for column in column_index_list:
        column_quote(tbl, column)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="column-select", help="カラムを選択")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="カラムのインデックスリスト。[index[,...]]")
def cmd_column_select(input: Optional[str], output: Optional[str], column: str) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    new_tbl = tbl.table_select_column_list(column_index_list)
    csv_file_writer(output_path, new_tbl)
    return 0


@click.command(name="column-sort", help="カラムでソート")
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
def cmd_column_sort(
    input: Optional[str], output: Optional[str], column_key: str, column_attr: Optional[str], header: int, reverse: bool
) -> int:
    """!
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


@click.command(name="csv-filetype", help="CSVファイルの種別を判定")
@click.option("--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def cmd_csv_filetype(csv_info_dir: str, files: tuple[str, ...]) -> int:
    """!
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


@click.command(name="csv-header-add", help="CSVファイルにヘッダを追加")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--add-header", type=click.Path(exists=True), required=True, help="追加するCSVヘッダファイル")
def cmd_csv_header_add(input: Optional[str], output: Optional[str], add_header: str) -> int:
    """!
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


@click.command(name="csv-header-change", help="CSVファイルのヘッダを変更")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--input-header", type=click.Path(exists=True), required=True, help="変更前CSVヘッダファイル")
@click.option("--output-header", type=click.Path(exists=True), required=True, help="変更後CSVヘッダファイル")
def cmd_csv_header_change(input: Optional[str], output: Optional[str], input_header: str, output_header) -> int:
    """!
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


@click.command(name="csv-header-del", help="CSVファイルのヘッダを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--header", type=int, required=True, help="ヘッダの行数")
def cmd_csv_header_del(input: Optional[str], output: Optional[str], header: int) -> int:
    """!
    @retval 0 正常終了
    @retval 1 異常終了
    """
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    tbl.table_header_del(header_count=header)
    csv_file_writer(output_path, tbl)
    return 0


@click.command(name="csv-report", help="CSVファイルの情報を表示")
@click.option("--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def cmd_csv_report(csv_info_dir: str, files: tuple[str, ...]) -> int:
    """!
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


cli.add_command(cmd_column_add)
cli.add_command(cmd_column_del)
cli.add_command(cmd_column_exclusive)
cli.add_command(cmd_column_fill)
cli.add_command(cmd_column_merge)
cli.add_command(cmd_column_move)
cli.add_command(cmd_column_quote)
cli.add_command(cmd_column_select)
cli.add_command(cmd_column_sort)
cli.add_command(cmd_csv_filetype)
cli.add_command(cmd_csv_header_add)
cli.add_command(cmd_csv_header_change)
cli.add_command(cmd_csv_header_del)
cli.add_command(cmd_csv_report)


def main(argv: list[str]) -> int:
    """!
    @brief 主入口点
    @param argv コマンドラインオプション
    @retval 0 成功
    @retval 1 失敗
    """
    rc = cli(standalone_mode=False)
    return rc


# if __name__ == "__main__":
#    sys.exit(main(sys.argv))
