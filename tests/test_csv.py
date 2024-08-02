# import pytest
import io

from src.csv import csv_reader
from src.table import Table


def test_csv_reader_0101N() -> None:
    test_data = """\
a,b,c
1,2,3
4,5,6
"""
    tbl: Table = csv_reader(io.StringIO(test_data))
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["1", "2", "3"]
    assert tbl._rows[2] == ["4", "5", "6"]


def test_csv_reader_0102N() -> None:  # ダブルクォート
    test_data = """\
a,"b1,b2",c
"""
    tbl: Table = csv_reader(io.StringIO(test_data))
    assert tbl._rows[0] == ["a", '"b1,b2"', "c"]
