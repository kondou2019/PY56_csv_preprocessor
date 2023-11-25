import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Optional

import click

__VERSION__ = "0.0.1"


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


def generate_alphabet_base26(index):
    """!
    @brief 26進数のアルファベットを生成する
    @note 注意。0は'A'ではなく、空文字列を返す。
    @param index 26進数の値。1から始まる。
    @return アルファベット
    """
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result  # 65 は 'A' のASCIIコード
    return result


def csv_writer_1(o_stream: TextIOWrapper, *, header_count: int = 0, column_count: int = 0, row_count: int = 0):
    """!
        @brief CSVファイルに書き込む
        @param o_stream 出力ストリーム
        @param header_count ヘッダの行数
        @param column_count カラム数
        @param row_count 行数
        @note 出力例
    A,B,C
    0,1,2
    0,1,2
    0,1,2
    """
    # ヘッダ行の出力
    for header_index in range(header_count):
        line = ",".join([generate_alphabet_base26(i) for i in range(1, column_count + 1)])
        o_stream.write(line)
        o_stream.write("\n")
    # データ行の出力
    for row_index in range(row_count):
        line = ",".join([str(i) for i in range(column_count)])
        o_stream.write(line)
        o_stream.write("\n")
    return


def csv_writer_2(o_stream: TextIOWrapper, *, header_count: int = 0, column_count: int = 0, row_count: int = 0):
    """!
        @brief CSVファイルに書き込む
        @detail セルの値が重複しないようにする。カラム数は99まで。
        @param o_stream 出力ストリーム
        @param header_count ヘッダの行数
        @param column_count カラム数
        @param row_count 行数
        @note 出力例
    A,B,C
    100,101,102
    200,201,202
    300,301,302
    """
    # ヘッダ行の出力
    for header_index in range(header_count):
        line = ",".join([generate_alphabet_base26(i) for i in range(1, column_count + 1)])
        o_stream.write(line)
        o_stream.write("\n")
    # データ行の出力
    row_index_base = 100
    for row_index in range(row_count):
        line = ",".join([str(i + row_index_base) for i in range(column_count)])
        o_stream.write(line)
        o_stream.write("\n")
        row_index_base += 100
    return


def csv_writer(type: str, o_stream: TextIOWrapper, *, header_count: int = 0, column_count: int = 0, row_count: int = 0):
    """!
    @brief CSVファイルに書き込む
    @param type 作成するデータの種類
    @param o_stream 出力ストリーム
    @param header_count ヘッダの行数
    @param column_count カラム数
    @param row_count 行数
    """
    #
    if type == "1":
        csv_writer_1(o_stream, header_count=header_count, column_count=column_count, row_count=row_count)
    elif type == "2":
        csv_writer_2(o_stream, header_count=header_count, column_count=column_count, row_count=row_count)
    return


@click.command(help="CSVファイルを作成")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--header-count", type=int, default=1, help="ヘッダの行数")
@click.option("--column-count", type=int, default=3, help="カラム数")
@click.option("--row-count", type=int, default=3, help="行数")
@click.option("--type", type=click.Choice(["1", "2"]), default="1", help="作成するデータの種類")
def make_csv(output: Optional[str], header_count: int, column_count: int, row_count: int, type: str) -> int:
    """!
    @brief カラムの選択
    @retval 0 正常終了
    @retval 1 異常終了
    """
    #
    _, output_path = option_path(None, output)
    # 実行
    if output_path is None:
        csv_writer(type, sys.stdout, header_count=header_count, column_count=column_count, row_count=row_count)
    else:
        with output_path.open(mode="w", encoding="utf-8") as o_stream:
            csv_writer(type, o_stream, header_count=header_count, column_count=column_count, row_count=row_count)
    return 0


# サブコマンドをメインコマンドに追加
@click.group(help="CSVファイルのテスト用ツール")
@click.version_option(version=__VERSION__)
def cli():
    pass


cli.add_command(make_csv)

if __name__ == "__main__":
    rc = cli(standalone_mode=False)
    sys.exit(rc)
