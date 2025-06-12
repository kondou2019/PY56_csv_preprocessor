import difflib
import io
import sys
from pathlib import Path
from typing import IO, Optional

from src.lib.common import split_csv_string_no_normalize
from src.lib.table import *


def _csv_reader(
    i_stream: IO[bytes], *, header: int = 0, csv_filetype: Optional[CsvFileTypeInfo] = None, strip: bool = False
) -> Table:
    """!
    @brief CSVファイルを読み込む
    @param i_stream 入力ストリーム;バイト入力
    @param header ヘッダの行数
    @param csv_filetype CSVファイルの情報
    @param strip 値の前後のスペースを除去
    @return 表
    """
    # 入力,全体を入力してパースする
    rows: list[list[str]] = []
    ## 改行コードの退避
    buf = i_stream.read()
    line_separator = b"\n"
    if b"\r\n" in buf:
        line_separator = b"\r\n"
    ## BOMの退避
    bom: Optional[bytes] = None
    if len(buf) >= 3 and buf[0:3] == b"\xEF\xBB\xBF":  # utf-8-sig
        bom = b"\xEF\xBB\xBF"
    ## 入力データを行入力
    bom_skip = 0
    if bom is not None:
        bom_skip = len(bom)
    for line in io.StringIO(buf[bom_skip:].decode(encoding="utf-8")):  # 入力データをストリーム化
        # 改行コードを削除
        line = line.rstrip("\r\n")
        columns = split_csv_string_no_normalize(line, strip=strip)
        rows.append(columns)
    # ヘッダ行の分離
    ## csv_filetypeのヘッダ行数が優先
    if csv_filetype is not None:
        header = csv_filetype.header_row_count
    ##
    if header > 0:
        header_rows = rows[:header]
        rows = rows[header:]
    ## tableの構築
    table = Table.create_rows(rows=rows)
    table._line_separator = line_separator
    table._bom = bom
    if header > 0:
        table._header_rows = header_rows
    ## csv_filetypeの情報と一致するか確認
    if csv_filetype is not None:
        if table._header_rows != csv_filetype._header_rows:
            data1 = [",".join(inner_list) for inner_list in table._header_rows]
            head1 = [",".join(inner_list) for inner_list in csv_filetype._header_rows]
            diff = difflib.ndiff(data1, head1)
            diff_s = "\n".join(diff)
            raise ValueError(f"ヘッダが一致しません。\n==差分==\n{diff_s}\n====\n")
    return table


def csv_string_reader(
    csv_str: str, *, header: int = 0, csv_filetype: Optional[CsvFileTypeInfo] = None, strip: bool = False
) -> Table:
    """!
    @brief _csv_reader()のstr用ラッパ
    @param csv_str CSV文字列
    """
    buffer = io.BytesIO()
    buffer.write(csv_str.encode())
    buffer.seek(0)
    return _csv_reader(buffer, header=header, csv_filetype=csv_filetype, strip=strip)


def csv_file_reader(file: Optional[Path], *, header: int = 0, csv_filetype: Optional[CsvFileTypeInfo] = None) -> Table:
    if file is None:
        stream = sys.stdin.buffer
        return _csv_reader(stream, header=header, csv_filetype=csv_filetype)
    #
    with file.open(mode="rb") as i_stream:
        return _csv_reader(i_stream, header=header, csv_filetype=csv_filetype)


def _csv_writer(o_stream: IO[bytes], table: Table) -> None:
    """!
    @brief CSVファイルに書き込む
    @param o_stream 出力ストリーム
    @param table 表
    """
    # BOM出力
    if table._bom is not None:
        o_stream.write(table._bom)
    # ヘッダ行の出力
    for row in table._header_rows:
        line = ",".join(row)
        o_stream.write(line.encode())
        o_stream.write(table._line_separator)  # 改行コードを回復
    # データ行の出力
    for row in table._rows:
        line = ",".join(row)
        o_stream.write(line.encode())
        o_stream.write(table._line_separator)  # 改行コードを回復
    return


def csv_file_writer(file: Optional[Path], table: Table) -> None:
    if file is None:
        stream = sys.stdout.buffer
        _csv_writer(stream, table)
        return
    #
    with file.open(mode="wb") as o_stream:
        _csv_writer(o_stream, table)
        return
