from dataclasses import dataclass
from typing import Optional

import click

from src.cmd_common import option_path
from src.csv import csv_file_reader, csv_file_writer
from src.table_utl import (
    column_exclusive_index_group,
    column_fill_index,
    column_merge_index_group,
    column_quote,
    column_replace_index,
    table_sort,
)


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
def cmd_column_add(input: Optional[str], output: Optional[str], column: str, column_count: int) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in sorted(column_index_list, reverse=True):  # カラムの最後から追加する
        tbl.table_column_add(column, column_count=column_count)
    csv_file_writer(output_path, tbl)
    return


@click.command(name="column-del", help="カラムを削除")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="削除するカラムのインデックスリスト。[index[,...]]")
def cmd_column_del(input: Optional[str], output: Optional[str], column: str) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in sorted(column_index_list, reverse=True):  # インデックスの大きい順に削除する
        tbl.table_column_del(column)
    csv_file_writer(output_path, tbl)
    return


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
def cmd_column_exclusive(input: Optional[str], output: Optional[str], column_group: tuple[str]) -> None:
    input_path, output_path = option_path(input, output)
    column_group_list = [option_index_list(i) for i in column_group]
    # 実行
    tbl = csv_file_reader(input_path)
    column_exclusive_index_group(tbl, column_group_list)
    csv_file_writer(output_path, tbl)
    return


@click.command(name="column-fill", help="カラムの欠損値を置換(穴埋め)")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="対象のカラムのインデックスリスト。[index[,...]]")
@click.option(
    "--value-source",
    type=click.Choice(["constant", "ffill", "column"]),
    default="constant",
    show_default=True,
    help="置換する値の元(--valueオプションと組み合わせる)。constant:指定値 ffill:前の行からの穴埋め column:指定したカラムの値",
)
@click.option(
    "--value",
    type=str,
    default="",
    show_default=True,
    help="置換する値。--value-sourceの指定値により意味が異なる。constant: セットする値 column: カラムのインデックス",
)
@click.option("--column-if", type=str, help="行のカラムの値に基づいて、置換を実行するかどうかを判定する")
def cmd_column_fill(
    input: Optional[str],
    output: Optional[str],
    column: str,
    value_source: str,
    value: str,
    column_if: Optional[str],
) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in column_index_list:
        column_fill_index(tbl, column, value_source, value, column_if=column_if)
    csv_file_writer(output_path, tbl)
    return


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
def cmd_column_merge(
    input: Optional[str], output: Optional[str], column_key: str, column_group: tuple[str, ...]
) -> None:
    input_path, output_path = option_path(input, output)
    column_key_index_list = option_index_list(column_key)
    column_group_list = [option_index_list(i) for i in column_group]
    # 実行
    tbl = csv_file_reader(input_path)
    column_merge_index_group(tbl, column_key_index_list, column_group_list)
    csv_file_writer(output_path, tbl)
    return


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
def cmd_column_move(from_: str, to: str, input: Optional[str], output: Optional[str]) -> None:
    input_path, output_path = option_path(input, output)
    from_column_index_list = option_index_list(from_)
    to_column_index_list = option_index_list(to)
    if len(from_column_index_list) != len(to_column_index_list):
        raise click.ClickException("--fromと--toに指定したインデックスの数が一致しません。")
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
    return


@click.command(name="column-quote", help="カラムの値をクォートで囲む")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="カラムのインデックスリスト。[index[,...]]")
def cmd_column_quote(input: Optional[str], output: Optional[str], column: str) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in column_index_list:
        column_quote(tbl, column)
    csv_file_writer(output_path, tbl)
    return


@click.command(name="column-replace", help="カラムの置換")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="対象のカラムのインデックスリスト。[index[,...]]")
@click.option("--regex", type=str, required=True, help="置換する正規表現")
@click.option("--repl", type=str, required=True, help="置換する文字列")
def cmd_column_replace(
    input: Optional[str],
    output: Optional[str],
    column: str,
    regex: str,
    repl: str,
) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    for column in column_index_list:
        column_replace_index(tbl, column, regex, repl)
    csv_file_writer(output_path, tbl)
    return


@click.command(name="column-select", help="カラムを選択")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option("--column", callback=custom_index_list, required=True, type=str, help="カラムのインデックスリスト。[index[,...]]")
def cmd_column_select(input: Optional[str], output: Optional[str], column: str) -> None:
    input_path, output_path = option_path(input, output)
    column_index_list = option_index_list(column)
    # 実行
    tbl = csv_file_reader(input_path)
    new_tbl = tbl.table_select_column_list(column_index_list)
    csv_file_writer(output_path, new_tbl)
    return


@click.command(name="column-sort", help="カラムでソート")
@click.option("--input", "-i", type=click.Path(exists=True), help="入力ファイル,省略時は標準入力")
@click.option("--output", "-o", type=click.Path(), help="出力ファイル,省略時は標準出力")
@click.option(
    "--column-key", callback=custom_index_list, required=True, type=str, help="ソートするカラムのインデックスリスト。[index[,...]]"
)
@click.option(
    "--column-attr", callback=custom_value_list, type=str, help="ソートするカラムの属性(str,int,float)。省略時はすべてstr。[attr[,...]]"
)
@click.option("--reverse", is_flag=True, help="降順にソート")
def cmd_column_sort(
    input: Optional[str], output: Optional[str], column_key: str, column_attr: Optional[str], reverse: bool
) -> None:
    input_path, output_path = option_path(input, output)
    column_key_index_list = option_index_list(column_key)
    if column_attr is None:
        column_attr_list = ["str"] * len(column_key_index_list)
    else:
        column_attr_list = option_value_list(column_attr)
    # 実行
    tbl = csv_file_reader(input_path)
    table_sort(tbl, set(column_key_index_list), column_attr_list, reverse=reverse)
    csv_file_writer(output_path, tbl)
    return
