from dataclasses import dataclass
from typing import Self

from src.filter.filter_base import FilterBase
from src.lib.table import Table


@dataclass(kw_only=True)
class SampleFilter(FilterBase):
    @classmethod
    def new_filter(cls) -> Self:
        return SampleFilter()

    def filter_execute(self, tbl: Table) -> Table:
        return tbl
