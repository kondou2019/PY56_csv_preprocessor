class Table:
    """!
    @brief 表のデータクラス
    """

    def __init__(self):
        """!
        @brief コンストラクタ
        """
        self._header_rows: list[list[str]] = []
        self._rows: list[list[str]] = []

    @classmethod
    def create_rows(cls, rows: list[list[str]]) -> "Table":
        """!
        @brief 表のデータを作成する
        @param rows 行のリスト
        @return 表のデータ
        """
        tbl = cls()
        tbl._rows = rows
        return tbl

    def column_add(self, column: list[str]) -> None:
        """!
        @brief 列を最後に追加する
        @param column 列
        """
        for i, row in enumerate(self._rows):
            row.append(column[i])

    def column_insert(self, column_index: int, column: list[str]) -> None:
        """!
        @brief 列を挿入する
        @param column_index 挿入する列の位置
        @param column 列
        """
        for i, row in enumerate(self._rows):
            row.insert(column_index, column[i])

    def column_insert_empty(self, column_index: int) -> None:
        """!
        @brief 空の列を挿入する
        @param column_index 挿入する列の位置
        """
        for row in self._rows:
            row.insert(column_index, "")

    def column_move(self, from_index: int, to_index: int) -> None:
        """!
        @brief 列を移動する
        @param from_index 移動元の列
        @param to_index 移動先の列
        """
        for row in self._rows:
            row.insert(to_index, row.pop(from_index))

    def column_remove(self, column_index: int) -> None:
        """!
        @brief 指定した列を削除する
        @param column_index 削除する列
        """
        for row in self._rows:
            row.pop(column_index)

    def row_add(self, row: list[str]) -> None:
        """!
        @brief 行を最後に追加する
        @param row 行
        """
        self._rows.append(row)

    def row_count(self) -> int:
        """!
        @brief 行数を取得する
        @return 行数
        """
        return len(self._rows)

    def row_duplicate(self, row_index: int) -> list[str]:
        """!
        @brief 行を複製する
        @param row_index 複製する行の位置
        @return 複製した行
        """
        duplicated_row = self._rows[row_index].copy()
        self._rows.insert(row_index + 1, duplicated_row)  # 次の行に挿入する
        return duplicated_row

    def row_insert(self, row_index: int, row: list[str]) -> None:
        """!
        @brief 行を挿入する
        @param row_index 挿入する行の位置
        @param row 行
        """
        self._rows.insert(row_index, row)

    def row_insert_empty(self, row_index: int) -> None:
        """!
        @brief 空の行を挿入する
        @param row_index 挿入する行の位置
        """
        self._rows.insert(row_index, [])  # TODO: カラム数分の空のリストを作成する

    def row_move(self, from_index: int, to_index: int) -> None:
        """!
        @brief 行を移動する
        @param from_index 移動元の行
        @param to_index 移動先の行
        """
        self._rows.insert(to_index, self._rows.pop(from_index))

    def row_remove(self, row_index: int) -> list[str]:
        """!
        @brief 指定した行を削除する
        @param row_index 削除する行
        @return 削除した行
        """
        return self._rows.pop(row_index)

    def row_remove_multi(self, start_row_index: int, end_row_index: int) -> list[list[str]]:
        """!
        @brief 指定した範囲の行を削除する
        @param row_index 削除する行
        @return 削除した行
        """
        removed_items = self._rows[start_row_index:end_row_index]
        del self._rows[start_row_index:end_row_index]
        return removed_items

    def table_select_column_range(self, start_index: int, end_index: int) -> "Table":
        """!
        @brief 指定した範囲の列を抽出する
        @param start_index 抽出する列の開始位置
        @param end_index 抽出する列の終了位置
        @return 抽出した表
        """
        tbl = Table()
        for row in self._rows:
            tbl.row_add(row[start_index:end_index])
        return tbl
