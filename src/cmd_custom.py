from pathlib import Path
from typing import Optional

import click

from src.cmd_common import option_path
from src.common import textfile_write
from src.csv import csv_file_reader, csv_file_writer
from src.table import Table


def make_header1(table: Table) -> str:
    """!
    @brief 1行ヘッダを作成
    @param table テーブル
    @return 1行ヘッダ
    """
    # 2行目から。前の行のカラムが空だったら直前のカラム名を埋める
    for row_index in range(1, table.row_count()):
        for column_index in range(table.column_count()):
            if table._rows[row_index - 1][column_index] == "":  # 前の行のカラムが空?
                if column_index > 0:
                    table._rows[row_index - 1][column_index] = table._rows[row_index - 1][
                        column_index - 1
                    ]  # 直前のカラム名で埋める
    # 1行ヘッダのカラム名の組み立て
    header_line1_list: list[str] = []
    for column_index in range(table.column_count()):
        column_name_list: list[str] = []
        for row_index in range(table.row_count()):
            v = table._rows[row_index][column_index]
            if v != "":
                column_name_list.append(v)
        header_line1_list.append("_".join(column_name_list))
    #
    return ",".join(header_line1_list)


@click.command(name="custom-header-get", help="カスタムヘッダの取得")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--separator", type=str, help="セパレータ。ヘッダの終端を表す文字列")
@click.option("--header", type=int, help="ヘッダの行数")
def cmd_custom_header_get(
    input: Optional[str], output: Optional[str], separator: Optional[str], header: Optional[int]
) -> None:
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    header_count = 0
    if separator is not None:
        for index, row in enumerate(tbl._rows):
            if row[0].startswith(separator):  # セパレータ
                header_count = index + 1  # 行数に変更。セパレータ行は含む
                break
    elif header is not None:
        header_count = header
    else:
        raise click.ClickException("--separator,--headerオプションのどちらかを指定してください。")
    tbl._rows = tbl._rows[:header_count]
    # 出力
    csv_file_writer(output_path, tbl)


@click.command(name="custom-header-line1", help="カスタムヘッダを1行ヘッダを作成")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--separator", type=str, help="セパレータ。ヘッダの終端を表す文字列")
@click.option("--header", type=int, help="ヘッダの行数")
def cmd_custom_header_line1(
    input: Optional[str], output: Optional[str], separator: Optional[str], header: Optional[int]
) -> None:
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    header_count = 0
    if separator is not None:
        for index, row in enumerate(tbl._rows):
            if row[0].startswith(separator):  # セパレータ
                header_count = index  # 行数に変更。セパレータ行は除く
                break
    elif header is not None:
        header_count = header
    else:
        raise click.ClickException("--separator,--headerオプションのどちらかを指定してください。")
    tbl._rows = tbl._rows[:header_count]
    #
    header = make_header1(tbl)
    textfile_write(output_path, [header + "\n"])
