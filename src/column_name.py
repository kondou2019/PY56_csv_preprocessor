from src.table import Table


class ColumnName:
    """!
    @brief カラムを名称で操作するためのクラス
    """

    def __init__(self, table: Table):
        """!
        @brief コンストラクタ
        """
        self._table: Table = table
        self._column_names: list[str] = []

    pass
