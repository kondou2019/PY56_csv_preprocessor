# import pytest
import io

from src.lib.csv import csv_string_reader
from src.lib.table import Table


def test_csv_string_reader_0101N() -> None:
    test_data = """\
a,b,c
1,2,3
4,5,6
"""
    tbl: Table = csv_string_reader(test_data)
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["1", "2", "3"]
    assert tbl._rows[2] == ["4", "5", "6"]


def test_csv_string_reader_0102N() -> None:  # ダブルクォート
    test_data = """\
a,"b1,b2",c
"""
    tbl: Table = csv_string_reader(test_data)
    assert tbl._rows[0] == ["a", '"b1,b2"', "c"]
