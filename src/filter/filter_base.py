from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Optional, Self

from src.lib.table import Table


class FilterType(Enum):
    TABLE = 1
    CELL = 2
    COLUMN = 3
    ROW = 4


class FilterBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def new_filter(cls, args: list[str]) -> Self:
        """!
        @brief Filterオブジェクトを作成
        @return Self
        """
        pass

    @classmethod
    @abstractmethod
    def filter_get_type(cls) -> FilterType:
        """!
        @brief フィルター種別の取得
        @retval FilterType
        """

    # @abstractmethod
    def filter_execute_table(self, table: Table, *, column_index_list: Optional[list[int]] = None) -> Table:
        """!
        @brief フィルター処理(Table)
        @param[in] table Table
        @param[in] column_index_list 対象のカラムのインデックスリスト
        @retval Table
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_cell(self, cell: str) -> str:
        """!
        @brief フィルター処理(cell)
        @param[in] cell セルの値
        @retval str
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_column(self, columns: list[str]) -> list[str]:
        """!
        @brief フィルター処理(columns)
        @param[in] columns 列
        @retval list[str]
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_row(self, rows: list[str]) -> Optional[list[str]]:
        """!
        @brief フィルター処理(rows)
        @param[in] rows 行
        @retval list[str]
        @retval None 削除
        """
        raise NotImplementedError()
