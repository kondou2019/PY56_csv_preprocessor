from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional, Self

from src.lib.table import Table


class FilterType(Enum):
    TABLE = 1
    CELL = 2
    COLUMNS = 3
    ROWS = 4


class FilterBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def new_filter(cls) -> Self:
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
    def filter_execute_table(self, table: Table, *, column_index_list: Optional[list[int]] = None, **kwargs) -> Table:
        """!
        @brief フィルター処理(Table)
        @param[in] table Table
        @param[in] column_index_list 対象のカラムのインデックスリスト
        @param[in] kwargs フィルターオプション
        @retval Table
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_cell(self, cell: str, **kwargs) -> str:
        """!
        @brief フィルター処理(cell)
        @param[in] cell セルの値
        @param[in] kwargs フィルターオプション
        @retval str
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_columns(self, columns: list[str], **kwargs) -> list[str]:
        """!
        @brief フィルター処理(columns)
        @param[in] columns 列
        @param[in] kwargs フィルターオプション
        @retval list[str]
        """
        raise NotImplementedError()

    # @abstractmethod
    def filter_execute_rows(self, rows: list[str], *, column_index_list: list[int] = [], **kwargs) -> list[str]:
        """!
        @brief フィルター処理(rows)
        @param[in] rows 行
        @param[in] column_index_list 対象のカラムのインデックスリスト
        @param[in] kwargs フィルターオプション
        @retval list[str]
        """
        raise NotImplementedError()
