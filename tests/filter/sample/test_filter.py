# import pytest
import io

from src.filter.sample.filter import SampleFilter
from src.lib.csv import csv_reader
from src.lib.table import Table


def test_execute():
    test_data = """\
a,b,c
1,2,3
4,5,6
"""
    tbl: Table = csv_reader(io.StringIO(test_data))
    filter = SampleFilter.new_filter()
    result = filter.filter_execute(tbl)
    assert result is not None
