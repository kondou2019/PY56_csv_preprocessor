# import pytest
import copy
import io

# from src.csv import csv_reader
from src.table import Table
from src.table_utl import (
    column_exclusive_index_group,
    column_fill_index,
    column_merge_index_group,
    table_sort,
    values_equal_index_group,
    values_non_empty,
    values_non_empty_index_group,
    values_set_empty,
    values_set_empty_index_group,
)

CSV_3x3 = """\
a,b,c
1,2,3
4,5,6
"""

TABLE_3x3 = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]


def test_values_equal_index_group_0101N():
    values1 = ["1", "2", "a"]
    values2 = ["1", "2", "b"]
    index_list = [0, 1]
    result = values_equal_index_group(values1, values2, index_list)
    assert result == True


def test_values_equal_index_group_0102A():
    values1 = ["1", "2", "a"]
    values2 = ["1", "2", "b"]
    index_list = [1, 2]
    result = values_equal_index_group(values1, values2, index_list)
    assert result == False


def test_values_non_empty_0101N():
    values = ["", "2", "3"]
    check_list = [0, 1, 2]
    result = values_non_empty(values, check_list)
    assert result == [1, 2]


def test_values_non_empty_0102B():  # valuesが空
    values = []
    check_list = [0, 1, 2]
    result = values_non_empty(values, check_list)
    assert result == []


def test_values_non_empty_0103N():  # すべて空
    values = ["", "", ""]
    check_list = [0, 1, 2]
    result = values_non_empty(values, check_list)
    assert result == []


def test_values_non_empty_index_group_0101N():
    values = ["", "2", "3"]
    index_group = [[0], [1], [2]]
    result = values_non_empty_index_group(values, index_group)
    assert result == [1, 2]


def test_values_non_empty_index_group_0102N():
    values = ["", "2", "3"]
    index_group = [[0, 1], [2]]
    result = values_non_empty_index_group(values, index_group)
    assert result == [0, 1]


def test_values_set_empty_0101N():
    values = ["1", "2", "3"]
    index_list = [1, 2]
    values_set_empty(values, index_list)
    assert values == ["1", "", ""]


def test_values_set_empty_index_group_0101N():
    values = ["1", "2", "3"]
    index_group = [[1], [2]]
    values_set_empty_index_group(values, index_group)
    assert values == ["1", "", ""]


def test_column_exclusive_index_group_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    column_exclusive_index_group(tbl, [[1], [2]])
    assert len(tbl._rows) == 6
    assert tbl._rows[0] == ["a", "b", ""]
    assert tbl._rows[1] == ["a", "", "c"]
    assert tbl._rows[2] == ["1", "2", ""]
    assert tbl._rows[3] == ["1", "", "3"]
    assert tbl._rows[4] == ["4", "5", ""]
    assert tbl._rows[5] == ["4", "", "6"]


def test_column_fill_index_0101N():  # すべて空
    LOCAL_TABLE_2x2 = [
        ["a", ""],
        ["b", ""],
        ["c", ""],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_2x2))
    column_fill_index(tbl, 1, "x")
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "x"]
    assert tbl._rows[1] == ["b", "x"]
    assert tbl._rows[2] == ["c", "x"]


def test_column_fill_index_0102N():  # 一部空
    LOCAL_TABLE_2x2 = [
        ["a", ""],
        ["b", "2"],
        ["c", ""],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_2x2))
    column_fill_index(tbl, 1, "x")
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "x"]
    assert tbl._rows[1] == ["b", "2"]
    assert tbl._rows[2] == ["c", "x"]


def test_column_fill_index_0201N():  # ffill,すべて空
    LOCAL_TABLE_2x2 = [
        ["a", ""],
        ["b", ""],
        ["c", ""],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_2x2))
    column_fill_index(tbl, 1, "", ffill=True)
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", ""]
    assert tbl._rows[1] == ["b", ""]
    assert tbl._rows[2] == ["c", ""]


def test_column_fill_index_0202N():  # ffill,一部空
    LOCAL_TABLE_2x2 = [
        ["a", ""],
        ["b", "2"],
        ["c", ""],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_2x2))
    column_fill_index(tbl, 1, "", ffill=True)
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", ""]
    assert tbl._rows[1] == ["b", "2"]
    assert tbl._rows[2] == ["c", "2"]


def test_column_fill_index_0203B():  # ffill,初期値を指定
    LOCAL_TABLE_2x2 = [
        ["a", ""],
        ["b", "2"],
        ["c", ""],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_2x2))
    column_fill_index(tbl, 1, "x", ffill=True)
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "x"]
    assert tbl._rows[1] == ["b", "2"]
    assert tbl._rows[2] == ["c", "2"]


def test_column_merge_index_group_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    column_exclusive_index_group(tbl, [[1], [2]])
    # マージ
    column_merge_index_group(tbl, [0], [[1], [2]])
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["1", "2", "3"]
    assert tbl._rows[2] == ["4", "5", "6"]


def test_column_merge_index_group_0102N():  # カラムグループ以外が一致
    TABLE_5x5 = [
        ["a", "b", "c", "d", "e"],
        ["11", "12", "", "14", "15"],
        ["11", "", "13", "14", "15"],
        ["21", "22", "23", "24", "25"],
    ]
    tbl = Table.create_rows(copy.deepcopy(TABLE_5x5))
    # マージ
    column_merge_index_group(tbl, [0], [[1], [2]])
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "b", "c", "d", "e"]
    assert tbl._rows[1] == ["11", "12", "13", "14", "15"]
    assert tbl._rows[2] == ["21", "22", "23", "24", "25"]


def test_column_merge_index_group_0103N():  # マージ済み
    TABLE_5x5 = [
        ["a", "b", "c", "d", "e"],
        ["11", "12", "13", "14", "15"],
        ["11", "12", "13", "14", "15"],
        ["21", "22", "23", "24", "25"],
    ]
    tbl = Table.create_rows(copy.deepcopy(TABLE_5x5))
    # マージ
    column_merge_index_group(tbl, [0], [[1], [2]])
    assert len(tbl._rows) == 4
    assert tbl._rows[0] == ["a", "b", "c", "d", "e"]
    assert tbl._rows[1] == ["11", "12", "13", "14", "15"]
    assert tbl._rows[2] == ["11", "12", "13", "14", "15"]
    assert tbl._rows[3] == ["21", "22", "23", "24", "25"]


def test_column_merge_index_group_0104B():  # カラムグループ以外が不一致でマージできない
    TABLE_5x5 = [
        ["a", "b", "c", "d", "e"],
        ["11", "12", "", "14", "15"],
        ["11", "", "13", "14", "99"],
        ["21", "22", "23", "24", "25"],
    ]
    tbl = Table.create_rows(copy.deepcopy(TABLE_5x5))
    # マージ
    column_merge_index_group(tbl, [0], [[1], [2]])
    assert len(tbl._rows) == 4
    assert tbl._rows[0] == ["a", "b", "c", "d", "e"]
    assert tbl._rows[1] == ["11", "12", "", "14", "15"]
    assert tbl._rows[2] == ["11", "", "13", "14", "99"]
    assert tbl._rows[3] == ["21", "22", "23", "24", "25"]


def test_table_sort_0101N():
    LOCAL_TABLE_3x3 = [
        ["a", "2", "21"],
        ["b", "1", "12"],
        ["c", "1", "11"],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_3x3))
    table_sort(tbl, {1, 2}, ["str", "str"])
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["c", "1", "11"]
    assert tbl._rows[1] == ["b", "1", "12"]
    assert tbl._rows[2] == ["a", "2", "21"]


def test_table_sort_0102N():  # 降順
    LOCAL_TABLE_3x3 = [
        ["c", "1", "11"],
        ["b", "1", "12"],
        ["a", "2", "21"],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_3x3))
    table_sort(tbl, {1, 2}, ["str", "str"], reverse=True)
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "2", "21"]
    assert tbl._rows[1] == ["b", "1", "12"]
    assert tbl._rows[2] == ["c", "1", "11"]


def test_table_sort_0201N():  # int
    LOCAL_TABLE_3x3 = [
        ["a", "1", "x"],
        ["b", "10", "y"],
        ["c", "2", "z"],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_3x3))
    table_sort(tbl, {1}, ["int"])
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "1", "x"]
    assert tbl._rows[1] == ["c", "2", "z"]
    assert tbl._rows[2] == ["b", "10", "y"]


def test_table_sort_0202N():  # float
    LOCAL_TABLE_3x3 = [
        ["a", "1.1", "x"],
        ["b", "10.2", "y"],
        ["c", "2.3", "z"],
    ]
    tbl = Table.create_rows(copy.deepcopy(LOCAL_TABLE_3x3))
    table_sort(tbl, {1}, ["float"])
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["a", "1.1", "x"]
    assert tbl._rows[1] == ["c", "2.3", "z"]
    assert tbl._rows[2] == ["b", "10.2", "y"]
