from pathlib import Path
from typing import Optional

import click


def custom_index_list(ctx: click.core.Context, param: click.Option, value: Optional[str]):
    """!
    @brief 独自のチェックを行う関数。インデックスリストのチェックを行う。
    """
    if value is None:
        return value
    if value[0] != "[" or value[-1] != "]":
        raise click.BadParameter('インデックスリストは"[index[,...]]"の形式である必要があります。')
    return value


def option_index_list(index_list: str) -> list[int]:
    """!
    @brief オプションのインデックスリストの共通処理を行う
    @param index_list インデックスリスト,"[index[,...]]"
    @return インデックスリスト
    """
    return [int(i) for i in index_list[1:-1].split(",")]


def option_path(input: Optional[str], output: Optional[str]) -> tuple[Optional[Path], Optional[Path]]:
    """!
    @brief オプションのパスの共通処理を行う
    @param input 入力ファイル
    @param output 出力ファイル
    @return 入力ファイルと出力ファイルのパス。Noneの場合は、標準入力と標準出力
    """
    input_path: Optional[Path] = None
    if input is not None:
        input_path = Path(input)
    output_path: Optional[Path] = None
    if output is not None:
        output_path = Path(output)
    return (input_path, output_path)
