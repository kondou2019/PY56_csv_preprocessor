import re
from dataclasses import dataclass
from typing import Optional, Self

import click

from src.filter.filter_base import FilterBase, FilterType
from src.lib.table import Table
from src.lib.table_utl import check_column_if


@dataclass(kw_only=True)
class RowDelFilter(FilterBase):
    @classmethod
    def new_filter(cls, args: list[str]) -> Self:
        ctx = parse_filter_option.make_context("row-del", args)
        x = parse_filter_option.invoke(ctx)
        return x

    @classmethod
    def filter_get_type(cls) -> FilterType:
        return FilterType.TABLE

    def __init__(self, *, column_if: Optional[str] = None):
        self.column_if = column_if

    def filter_execute_table(self, table: Table, *, column_index_list: Optional[list[int]] = None) -> Table:
        # パラメタの設定
        column_if = self.column_if  # 0=='4'
        # column_ifのセットアップ
        if column_if is not None:
            match = re.match(r"(\d+)([!=><]=?)(.*)", column_if)
            if match is None:
                raise Exception(f"--column-ifの指定が正しくありません。--raw-if {column_if}")
            column_if_index = int(match.group(1))  # 先頭の数字部分
            column_if_operator = match.group(2)  # 比較演算子
            column_if_rest = match.group(3)  # 残りの文字列
            # 指定値の正規化
            column_if_index = int(column_if_index)
            ## 右辺の正規化
            match = re.search(r'(["\'])(.*?)\1', column_if_rest)
            if match:
                column_if_rest = match.group(2)  # クォート内の文字列を取得
        # 実行
        for i in range(table.row_count() - 1, -1, -1):
            row = table._rows[i]
            v_left = row[column_if_index]
            if check_column_if(v_left, column_if_operator, column_if_rest, column_if=column_if) == False:
                continue
            table.row_remove(i)

        return table


@click.command(name="row_del", help="行の削除")
@click.option("--column-if", type=str, required=True, help="行のカラムの値に基づいて、行の削除を実行するかどうかを判定する")
def parse_filter_option(
    column_if: Optional[str],
) -> RowDelFilter:
    x = RowDelFilter(column_if=column_if)
    return x
