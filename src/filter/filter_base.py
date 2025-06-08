from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional, Self

from src.lib.table import Table


class FilterBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def new_filter(cls) -> Self:
        """!
        @brief Filterオブジェクトを作成
        @return Self
        """
        pass

    @abstractmethod
    def filter_execute(self, table: Table) -> Table:
        """!
        @brief フィルター処理
        @param[in] driver
        @param[in] url
        @retval (0, htmlテキスト) 成功
        @retval (1, None) 失敗
        """
