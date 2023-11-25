# import pytest
import io

from src.csv import csv_reader
from src.table import Table


def test_csv_reader_0101():
    test_data = """\
a,b,c
1,2,3
4,5,6
"""
    tbl: Table = csv_reader(io.StringIO(test_data))
    pass
