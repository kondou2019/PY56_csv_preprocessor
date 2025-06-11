import re
from dataclasses import dataclass
from typing import Self

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
    def new_filter(cls) -> Self:
        return MultiValueFilter()

    @classmethod
    def filter_get_type(cls) -> FilterType:
        return FilterType.CELL

    def filter_execute_cell(self, cell: str, **kwargs) -> str:
        # パラメタの設定
        regex = kwargs["regex"]  # "^a$"
        repl = kwargs["repl"]  # "x"

        # 分割
        column_value = cell
        (column_value_list, quote) = multi_value_split(column_value)

        # 置換
        for i, v in enumerate(column_value_list):
            column_value_list[i] = re.sub(regex, repl, v)

        # 重複排除
        column_value_list = list(dict.fromkeys(column_value_list))

        # 結合
        result = multi_value_join(column_value_list, quote)
        return result
