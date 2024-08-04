# import pytest
import copy
import io

from src.table import Table

TABLE_3x3 = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]


def test_create_rows_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    assert tbl.row_count() == 3


def test_column_add_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.column_add(["A", "B", "C"])
    assert tbl._rows[0] == ["a", "b", "c", "A"]
    assert tbl._rows[1] == ["1", "2", "3", "B"]
    assert tbl._rows[2] == ["4", "5", "6", "C"]


def test_column_insert_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.column_insert(column_index=1, column=["A", "B", "C"])
    assert tbl._rows[0] == ["a", "A", "b", "c"]
    assert tbl._rows[1] == ["1", "B", "2", "3"]
    assert tbl._rows[2] == ["4", "C", "5", "6"]


def test_column_insert_empty_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.column_insert_empty(column_index=1)
    assert tbl._rows[0] == ["a", "", "b", "c"]
    assert tbl._rows[1] == ["1", "", "2", "3"]
    assert tbl._rows[2] == ["4", "", "5", "6"]


def test_column_move_0101N():  # 後ろに移動
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.column_move(from_index=0, to_index=2)
    assert tbl._rows[0] == ["b", "c", "a"]
    assert tbl._rows[1] == ["2", "3", "1"]
    assert tbl._rows[2] == ["5", "6", "4"]


def test_column_move_0102N():  # 前に移動
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.column_move(from_index=2, to_index=0)
    assert tbl._rows[0] == ["c", "a", "b"]
    assert tbl._rows[1] == ["3", "1", "2"]
    assert tbl._rows[2] == ["6", "4", "5"]


def test_column_remove_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    result = tbl.column_remove(column_index=1)
    assert result == ["b", "2", "5"]

    assert tbl._rows[0] == ["a", "c"]
    assert tbl._rows[1] == ["1", "3"]
    assert tbl._rows[2] == ["4", "6"]


def test_row_count_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    assert tbl.row_count() == 3


def test_row_add_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_add(["A", "B", "C", "D"])
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["1", "2", "3"]
    assert tbl._rows[2] == ["4", "5", "6"]
    assert tbl._rows[3] == ["A", "B", "C", "D"]


def test_row_duplicate_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    row1 = tbl._rows[1]
    tbl.row_duplicate(row_index=1)
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["1", "2", "3"]
    assert tbl._rows[2] == ["1", "2", "3"]
    assert tbl._rows[3] == ["4", "5", "6"]
    # 複製行の内容を変更しても、元の行には影響しないか確認する
    tbl._rows[2][0] = "z"
    assert tbl._rows[1][0] == "1"
    assert tbl._rows[2][0] == "z"
    # 元の行の内容を変更しても、複製行には影響しないか確認する
    row1[0] = "x"
    assert tbl._rows[1] == ["x", "2", "3"]


def test_row_insert_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_insert(row_index=1, row=["A", "B", "C"])
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["A", "B", "C"]
    assert tbl._rows[2] == ["1", "2", "3"]
    assert tbl._rows[3] == ["4", "5", "6"]


def test_row_insert_empty_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_insert_empty(row_index=1)
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == []
    assert tbl._rows[2] == ["1", "2", "3"]
    assert tbl._rows[3] == ["4", "5", "6"]


def test_row_move_0101N():  # 後ろに移動
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_move(from_index=0, to_index=2)
    assert tbl._rows[0] == ["1", "2", "3"]
    assert tbl._rows[1] == ["4", "5", "6"]
    assert tbl._rows[2] == ["a", "b", "c"]


def test_row_move_0102N():  # 前に移動
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_move(from_index=2, to_index=0)
    assert tbl._rows[0] == ["4", "5", "6"]
    assert tbl._rows[1] == ["a", "b", "c"]
    assert tbl._rows[2] == ["1", "2", "3"]


def test_row_remove_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    result = tbl.row_remove(row_index=1)
    assert result == ["1", "2", "3"]

    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["4", "5", "6"]


def test_row_remove_multi_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl.row_remove_multi(start_row_index=1, end_row_index=2)
    assert len(tbl._rows) == 2
    assert tbl._rows[0] == ["a", "b", "c"]
    assert tbl._rows[1] == ["4", "5", "6"]


def test_table_select_column_range_0101N():
    tbl = Table.create_rows(copy.deepcopy(TABLE_3x3))
    tbl = tbl.table_select_column_range(start_index=1, end_index=2)
    assert len(tbl._rows) == 3
    assert tbl._rows[0] == ["b"]
    assert tbl._rows[1] == ["2"]
    assert tbl._rows[2] == ["5"]
