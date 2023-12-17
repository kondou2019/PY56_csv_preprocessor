from typing import TypeVar

from src.table import Table

Self = TypeVar("Self", bound="ColumnName")


class ColumnName:
    """!
    @brief カラムを名称で操作するためのクラス
    """

    def __init__(self: Self, table: Table):
        """!
        @brief コンストラクタ
        """
        self._table: Table = table
        self._column_names: list[str] = []

    pass
