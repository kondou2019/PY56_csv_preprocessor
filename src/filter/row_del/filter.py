import re
from dataclasses import dataclass
from typing import Optional, Self

import click

from src.filter.filter_base import FilterBase, FilterType
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
        return FilterType.ROW

    def __init__(self, *, column_if: Optional[str] = None):
        self.column_if = column_if
        # column_ifのセットアップ
        if column_if is not None:
            match = re.match(r"(\d+)([!=><]=?)(.*)", column_if)
            if match is None:
                raise Exception(f"--column-ifの指定が正しくありません。--raw-if {column_if}")
            self.column_if_index = int(match.group(1))  # 先頭の数字部分
            self.column_if_operator = match.group(2)  # 比較演算子
            self.column_if_rest = match.group(3)  # 残りの文字列
            # 指定値の正規化
            self.column_if_index = int(self.column_if_index)
            ## 右辺の正規化
            match = re.search(r'(["\'])(.*?)\1', self.column_if_rest)
            if match:
                self.column_if_rest = match.group(2)  # クォート内の文字列を取得

    def filter_execute_row(self, row: list[str]) -> Optional[list[str]]:
        # 実行
        v_left = row[self.column_if_index]
        if check_column_if(v_left, self.column_if_operator, self.column_if_rest, column_if=self.column_if) == True:
            return None
        return row


@click.command(name="row_del", help="行の削除")
@click.option("--column-if", type=str, required=True, help="行のカラムの値に基づいて、行の削除を実行するかどうかを判定する")
def parse_filter_option(
    column_if: Optional[str],
) -> RowDelFilter:
    x = RowDelFilter(column_if=column_if)
    return x
