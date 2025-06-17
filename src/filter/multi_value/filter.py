import re
from dataclasses import dataclass
from typing import Optional, Self

import click

from src.filter.filter_base import FilterBase, FilterType
from src.lib.table import Table


def multi_value_join(v: list[str], quote: bool) -> str:
    """!
    @brief 複数値(セルに複数の値を指定)を結合
    @param v セルの文字列
    @param quote クォートの有無。True: クォートあり, False: クォートなし
    @retval 結合した文字列
    """
    if quote == False:
        assert len(v) == 1
        return v[0]
    return f'"{",".join(v)}"'


def multi_value_split(v: str) -> tuple[list[str], bool]:
    """!
    @brief 複数値(セルに複数の値を指定)を分割
    @param v セルの文字列
    @retval #0 分割された文字列リスト
    @retval #1 クォートの有無。True: クォートあり, False: クォートなし
    """
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':  # 既にクォートで囲んでいる?
        pass
    else:
        return ([v], False)
    v0 = v[1:-1]  # クォートを除去
    result = v0.split(",")
    return (result, True)


def multi_value_replace(
    table: Table,
    column_index: int,
    regex: str,
    repl: str,
):
    """!
    @brief カラムを置換する
    @param table テーブル
    @param column_index カラムのインデックス
    @param regex 置換を実行する正規表現
    @param repl 置換する文字列
    """
    #
    for row in table._rows:
        column_value = row[column_index]
        (column_value_list, quote) = multi_value_split(column_value)
        for i, v in enumerate(column_value_list):
            column_value_list[i] = re.sub(regex, repl, v)
        row[column_index] = multi_value_join(column_value_list, quote)
    pass


@dataclass(kw_only=True)
class MultiValueFilter(FilterBase):
    @classmethod
    def new_filter(cls, args: list[str]) -> Self:
        ctx = parse_filter_option.make_context("multi-view", args)
        x = parse_filter_option.invoke(ctx)
        return x

    @classmethod
    def filter_get_type(cls) -> FilterType:
        return FilterType.CELL

    def __init__(self, *, regex: str, repl: str, uniq: bool = False, empty_remove: bool = False):
        self.regex = regex
        self.repl = repl
        self.uniq = uniq
        self.empty_remove = empty_remove

    def filter_execute_cell(self, cell: str) -> str:
        # パラメタの設定
        regex = self.regex  # "^a$"
        repl = self.repl  # "x"
        uniq = self.uniq
        empty_remove = self.empty_remove

        # 分割
        column_value = cell
        (column_value_list, quote) = multi_value_split(column_value)

        # 置換
        for i, v in enumerate(column_value_list):
            column_value_list[i] = re.sub(regex, repl, v)

        # 重複排除
        if uniq == True:
            column_value_list = list(dict.fromkeys(column_value_list))

        # 空文字削除
        if empty_remove == True:
            column_value_list = [x for x in column_value_list if x != ""]

        # 結合
        result = multi_value_join(column_value_list, quote)
        return result


@click.command(name="multi_view", help="複数値")
@click.option("--regex", type=str, required=True, help="置換する正規表現")
@click.option("--repl", type=str, required=True, help="置換する文字列")
@click.option("--uniq", is_flag=True, help="重複排除")
@click.option("--empty-remove", is_flag=True, help="空値削除")
def parse_filter_option(regex: str, repl: str, uniq: bool, empty_remove: bool) -> MultiValueFilter:
    x = MultiValueFilter(regex=regex, repl=repl, uniq=uniq, empty_remove=empty_remove)
    return x
