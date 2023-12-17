from dataclasses import dataclass, field
from typing import Type, TypeVar


@dataclass
class CsvFileTypeInfo:
    """!
    @brief CSVファイルの種別情報
    """

    type_name: str
    header_lines: list[str] = field(default_factory=list)
    header_column_count: int = 0
    header_row_count: int = 0
    _header_rows: list[list[str]] = field(default_factory=list)


Self = TypeVar("Self", bound="Table")


class Table:
    """!
    @brief 表のデータクラス
    """

    def __init__(self: Self):
        """!
        @brief コンストラクタ
        """
        self._header_rows: list[list[str]] = []
        self._rows: list[list[str]] = []

    @classmethod
    def create_rows(cls: Type[Self], rows: list[list[str]]) -> Self:
        """!
        @brief 表のデータを作成する
        @param rows 行のリスト
        @return 表のデータ
        """
        tbl = cls()
        tbl._rows = rows
        return tbl

    def column_add(self: Self, column: list[str]) -> None:
        """!
        @brief 列を最後に追加する
        @param column 列
        """
        for i, row in enumerate(self._rows):
            row.append(column[i])

    def column_count(self: Self) -> int:
        """!
        @brief カラムの数を取得する
        @return カラム数
        """
        return len(self._rows[0])

    def column_insert(self: Self, column_index: int, column: list[str]) -> None:
        """!
        @brief 列を挿入する
        @param column_index 挿入する列の位置
        @param column 列
        """
        for i, row in enumerate(self._rows):
            row.insert(column_index, column[i])

    def column_insert_empty(self: Self, column_index: int) -> None:
        """!
        @brief 空の列を挿入する
        @param column_index 挿入する列の位置
        """
        for row in self._rows:
            row.insert(column_index, "")

    def column_move(self: Self, from_index: int, to_index: int) -> None:
        """!
        @brief 列を移動する
        @param from_index 移動元の列
        @param to_index 移動先の列
        """
        for row in self._rows:
            row.insert(to_index, row.pop(from_index))

    def column_remove(self: Self, column_index: int) -> None:
        """!
        @brief 指定した列を削除する
        @param column_index 削除する列
        """
        for row in self._rows:
            row.pop(column_index)

    def row_add(self: Self, row: list[str]) -> None:
        """!
        @brief 行を最後に追加する
        @param row 行
        """
        self._rows.append(row)

    def row_count(self: Self) -> int:
        """!
        @brief 行数を取得する
        @return 行数
        """
        return len(self._rows)

    def row_duplicate(self: Self, row_index: int) -> list[str]:
        """!
        @brief 行を複製する
        @param row_index 複製する行の位置
        @return 複製した行
        """
        duplicated_row = self._rows[row_index].copy()
        self._rows.insert(row_index + 1, duplicated_row)  # 次の行に挿入する
        return duplicated_row

    def row_insert(self: Self, row_index: int, row: list[str]) -> None:
        """!
        @brief 行を挿入する
        @param row_index 挿入する行の位置
        @param row 行
        """
        self._rows.insert(row_index, row)

    def row_insert_empty(self: Self, row_index: int) -> None:
        """!
        @brief 空の行を挿入する
        @param row_index 挿入する行の位置
        """
        self._rows.insert(row_index, [])  # TODO: カラム数分の空のリストを作成する

    def row_move(self: Self, from_index: int, to_index: int) -> None:
        """!
        @brief 行を移動する
        @param from_index 移動元の行
        @param to_index 移動先の行
        """
        self._rows.insert(to_index, self._rows.pop(from_index))

    def row_remove(self: Self, row_index: int) -> list[str]:
        """!
        @brief 指定した行を削除する
        @param row_index 削除する行
        @return 削除した行
        """
        return self._rows.pop(row_index)

    def row_remove_multi(self: Self, start_row_index: int, end_row_index: int) -> list[list[str]]:
        """!
        @brief 指定した範囲の行を削除する
        @param start_row_index 削除する開始インデックス
        @param end_row_index 削除する終了インデックス※終了インデックスは含まない
        @return 削除した行
        """
        removed_items = self._rows[start_row_index:end_row_index]
        del self._rows[start_row_index:end_row_index]
        return removed_items

    def table_column_add(self: Self, column_index: int) -> None:
        """!
        @brief カラムを追加
        @param column_index 追加するカラム(インデックス)。インデックスの前に追加する。最後に追加する場合は、-1を指定する。
        """
        if column_index < 0:
            for columns in self._rows:
                columns.append("")
        else:
            for columns in self._rows:
                columns.insert(column_index, "")

    def table_column_del(self: Self, column_index: int) -> None:
        """!
        @brief カラムを削除
        @param column_index 削除するカラム(インデックス)
        """
        for columns in self._rows:
            del columns[column_index]

    def table_header_add(self: Self, csv_filetype: CsvFileTypeInfo) -> None:
        """!
        @brief テーブルにヘッダを追加
        @param csv_filetype ヘッダ情報
        @exception ValueError 追加するCSVヘッダとカラム数が一致しない場合
        """
        # 追加するCSVヘッダとカラム数が一致するか確認
        if self.column_count() != csv_filetype.header_column_count:
            raise ValueError("追加するCSVヘッダとカラム数が一致しません。")
        #
        self._header_rows = csv_filetype._header_rows  # ヘッダを追加

    def table_header_del(self: Self, *, header_count: int = 0) -> None:
        """!
        @brief テーブルのヘッダを取り除く
        @param header_count ヘッダの行数
        """
        if len(self._header_rows) != 0:
            self._header_rows = []
        else:
            self.row_remove_multi(0, header_count)

    def table_select_column_range(self: Self, start_index: int, end_index: int) -> Self:
        """!
        @brief 指定した範囲の列を抽出する
        @param start_index 抽出する列の開始位置
        @param end_index 抽出する列の終了位置
        @return 抽出した表
        """
        tbl = type(self)()
        for row in self._rows:
            tbl.row_add(row[start_index:end_index])
        return tbl
