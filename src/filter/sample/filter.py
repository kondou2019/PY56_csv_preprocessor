from dataclasses import dataclass
from typing import Optional, Self

from src.filter.filter_base import FilterBase, FilterType
from src.lib.table import Table


@dataclass(kw_only=True)
class SampleFilter(FilterBase):
    @classmethod
    def new_filter(cls) -> Self:
        return SampleFilter()

    @classmethod
    def filter_get_type(cls) -> FilterType:
        return FilterType.TABLE

    def filter_execute_table(self, table: Table, *, column_index_list: Optional[list[int]] = None, **kwargs) -> Table:
        return table
