# import pytest
import io

from src.column_name import ColumnName
from src.csv import csv_reader
from src.table import Table

CSV_3x3 = """\
a,b,c
1,2,3
4,5,6
"""


def test_column_name_0101N() -> None:
    tbl: Table = csv_reader(io.StringIO(CSV_3x3))
    header = tbl._rows[0]
    tbl.row_remove(0)  # ヘッダーを削除
    cn = ColumnName(tbl)
    cn._column_names = header
    #
    for row_index in range(tbl.row_count()):
        columns = tbl._rows[row_index]
        if columns[1] == "2":
            tbl.row_duplicate(row_index)
            tbl._rows[row_index][2] = ""
            tbl._rows[row_index + 1][1] = ""
            pass

    pass
