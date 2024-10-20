# import pytest
import io

from src.cmd_custom import make_header1
from src.csv import csv_reader
from src.table import Table


def test_make_header1_0101N() -> None:
    test_data = """\
name,val,c11 ,   ,    ,   ,c12 ,
    ,   ,name,val,c21 ,   ,name,val
    ,   ,    ,   ,name,val,    ,
"""
    tbl: Table = csv_reader(io.StringIO(test_data), strip=True)
    result = make_header1(tbl)
    assert result == "name,val,c11_name,c11_val,c11_c21_name,c11_c21_val,c12_name,c12_val"


def test_make_header1_0102N() -> None:
    test_data = """\
name,val,c11 ,   ,    ,   ,c12 ,   ,    ,
    ,   ,name,val,c21 ,   ,name,val,c22 ,
    ,   ,    ,   ,name,val,    ,   ,name,val
"""
    tbl: Table = csv_reader(io.StringIO(test_data), strip=True)
    result = make_header1(tbl)
    assert result == "name,val,c11_name,c11_val,c11_c21_name,c11_c21_val,c12_name,c12_val,c12_c22_name,c12_c22_val"
