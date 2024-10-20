from pathlib import Path
from typing import Optional

import click

from src.cmd_common import option_path
from src.csv import csv_file_reader, csv_file_writer


@click.command(name="custom-header-get", help="カスタムヘッダの取得")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
def cmd_custom_header_get(input: Optional[str], output: Optional[str]) -> None:
    input_path, output_path = option_path(input, output)
    # 実行
    tbl = csv_file_reader(input_path)
    for index, row in enumerate(tbl._rows):
        if row[0].startswith("=="):  # セパレータ
            tbl._rows = tbl._rows[: index + 1]
            break
    csv_file_writer(output_path, tbl)
