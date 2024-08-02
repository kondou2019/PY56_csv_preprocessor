import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Optional

from src.common import split_csv_string_no_normalize
from src.table import *


def csv_reader(i_stream: TextIOWrapper, *, header: int = 0, csv_filetype: Optional[CsvFileTypeInfo] = None) -> Table:
    """!
    @brief CSVファイルを読み込む
    @param i_stream 入力ストリーム
    @param header ヘッダの行数
    @param csv_filetype CSVファイルの情報
    @return 表
    """
    rows: list[list[str]] = []
    for line in i_stream:
        line = line.rstrip("\n")
        # columns = line.split(",")
        columns = split_csv_string_no_normalize(line)
        rows.append(columns)
    # csv_filetypeのヘッダ行数が優先
    if csv_filetype is not None:
        header = csv_filetype.header_row_count
    #
    if header > 0:
        header_rows = rows[:header]
        rows = rows[header:]
    table = Table.create_rows(rows=rows)
    if header > 0:
        table._header_rows = header_rows
    # csv_filetypeの情報と一致するか確認
    if csv_filetype is not None:
        if table._header_rows != csv_filetype._header_rows:
            raise ValueError("ヘッダが一致しません。")
    return table


def csv_file_reader(file: Optional[Path], *, header: int = 0, csv_filetype: Optional[CsvFileTypeInfo] = None) -> Table:
    if file is None:
        stream = TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        return csv_reader(stream, header=header, csv_filetype=csv_filetype)
    #
    with file.open(mode="r", encoding="utf-8") as i_stream:
        return csv_reader(i_stream, header=header, csv_filetype=csv_filetype)


def csv_writer(o_stream: TextIOWrapper, table: Table):
    """!
    @brief CSVファイルに書き込む
    @param o_stream 出力ストリーム
    @param table 表
    """
    # ヘッダ行の出力
    for row in table._header_rows:
        line = ",".join(row)
        o_stream.write(line)
        o_stream.write("\n")
    # データ行の出力
    for row in table._rows:
        line = ",".join(row)
        o_stream.write(line)
        o_stream.write("\n")
    return


def csv_file_writer(file: Optional[Path], table: Table):
    if file is None:
        stream = TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        return csv_writer(stream, table)
    #
    with file.open(mode="w", encoding="utf-8") as o_stream:
        return csv_writer(o_stream, table)
