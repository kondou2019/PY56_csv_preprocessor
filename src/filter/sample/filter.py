from dataclasses import dataclass
from typing import Optional, Self

import click

from src.filter.filter_base import FilterBase, FilterType
from src.lib.table import Table


@dataclass(kw_only=True)
class SampleFilter(FilterBase):
    @classmethod
    def new_filter(cls, args: list[str]) -> Self:
        ctx = parse_filter_option.make_context("sample", args)
        x = parse_filter_option.invoke(ctx)
        return x

    @classmethod
    def filter_get_type(cls) -> FilterType:
        return FilterType.TABLE

    def filter_execute_table(self, table: Table, *, column_index_list: Optional[list[int]] = None) -> None:
        return


@click.command(name="sample", help="フィルタサンプル")
def parse_filter_option() -> SampleFilter:
    x = SampleFilter()
    return x
