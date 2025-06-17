# import pytest

from src.filter.sample.filter import SampleFilter
from src.lib.csv import csv_string_reader
from src.lib.table import Table


def test_filter_execute_table() -> None:
    test_data = """\
a,b,c
1,2,3
4,5,6
"""
    tbl: Table = csv_string_reader(test_data)
    filter = SampleFilter.new_filter([])
    result = filter.filter_execute_table(tbl)
    assert result is not None
