import json
import sys
from pathlib import Path
from typing import Optional

import click

from src.cmd_common import option_path
from src.csv import csv_file_reader, csv_file_writer
from src.table_utl import (
    CsvFileTypeInfo,
    CsvReportInfo,
    csv_filetype_detect,
    csv_filetype_list_read,
    csv_filetype_read,
    table_report,
)


@click.command(name="csv-filetype", help="CSVファイルの種別を判定")
@click.option(
    "--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ。ヘッダ情報ファイルは*_header.csvであること"
)
@click.argument("files", type=str, nargs=-1, required=True)
def cmd_csv_filetype(csv_info_dir: str, files: tuple[str, ...]) -> None:
    csv_info_dir_path = Path(csv_info_dir)
    # CSV種別のリストを作成
    csv_type_list = csv_filetype_list_read(csv_info_dir_path)
    if len(csv_type_list) == 0:
        print("CSV情報ファイルが見つかりません。", file=sys.stderr)
        sys.exit(1)
    # ファイルの種別判定
    for file in files:
        file_path = Path(file)
        #
        csv_type = csv_filetype_detect(csv_type_list, file_path)
        if csv_type is not None:
            print(f"{file}\t{csv_type.type_name}")
        else:
            print(f"{file}\t***unknown***")
    return


@click.command(name="csv-header-add", help="CSVファイルにヘッダを追加")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--add-header", type=click.Path(exists=True), required=True, help="追加するCSVヘッダファイル")
def cmd_csv_header_add(input: Optional[str], output: Optional[str], add_header: str) -> None:
    input_path, output_path = option_path(input, output)
    add_header_path = Path(add_header)
    # 実行
    add_csv_filetype = csv_filetype_read(add_header_path)  # 追加するCSVヘッダファイルを読み込む
    tbl = csv_file_reader(input_path)
    tbl.table_header_add(add_csv_filetype)
    csv_file_writer(output_path, tbl)

    return


@click.command(name="csv-header-change", help="CSVファイルのヘッダを変更")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--input-header", type=click.Path(exists=True), required=True, help="変更前CSVヘッダファイル")
@click.option("--output-header", type=click.Path(exists=True), required=True, help="変更後CSVヘッダファイル")
def cmd_csv_header_change(input: Optional[str], output: Optional[str], input_header: str, output_header) -> None:
    input_path, output_path = option_path(input, output)
    # CSVヘッダファイルの種別を読み込む
    input_csv_filetype = csv_filetype_read(Path(input_header))
    output_csv_filetype = csv_filetype_read(Path(output_header))
    # 実行
    tbl = csv_file_reader(input_path, csv_filetype=input_csv_filetype)
    tbl.table_header_del()  # ヘッダを削除
    tbl.table_header_add(output_csv_filetype)  # 新しいヘッダを追加
    csv_file_writer(output_path, tbl)
    return


@click.command(name="csv-header-del", help="CSVファイルのヘッダを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--input-header", type=click.Path(exists=True), help="変更前CSVヘッダファイル")
@click.option("--header", type=int, help="ヘッダの行数")
def cmd_csv_header_del(
    input: Optional[str], output: Optional[str], input_header: Optional[str], header: Optional[int]
) -> None:
    input_path, output_path = option_path(input, output)
    # CSVヘッダファイルの種別を読み込む
    header_count = 0
    input_csv_filetype: Optional[CsvFileTypeInfo] = None
    if input_header is not None:
        input_csv_filetype = csv_filetype_read(Path(input_header))
        header_count = input_csv_filetype.header_row_count
    elif header is not None:
        header_count = header
    else:
        raise click.ClickException("--input-header,--headerオプションのどちらかを指定してください。")
    # 実行
    tbl = csv_file_reader(input_path, csv_filetype=input_csv_filetype)

    tbl.table_header_del(header_count=header_count)
    csv_file_writer(output_path, tbl)
    return


@click.command(name="csv-report", help="CSVファイルの情報を表示")
@click.option("--csv-info-dir", type=click.Path(exists=True), required=True, help="CSV情報ファイルのディレクトリ")
@click.argument("files", type=str, nargs=-1, required=True)
def cmd_csv_report(csv_info_dir: str, files: tuple[str, ...]) -> None:
    csv_info_dir_path = Path(csv_info_dir)
    # CSV種別のリストを作成
    csv_type_list = csv_filetype_list_read(csv_info_dir_path)
    if len(csv_type_list) == 0:
        print("CSV情報ファイルが見つかりません。", file=sys.stderr)
        sys.exit(1)
    # ファイルのレポートを作成
    csv_report_info_list: list[CsvReportInfo] = []
    for file in files:
        file_path = Path(file)
        #
        report_info = table_report(csv_type_list, file_path)
        csv_report_info_list.append(report_info)
    # ファイルの情報をJSON形式で表示
    print(json.dumps([x.__dict__ for x in csv_report_info_list], indent=2))
    return
