import io
import itertools
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from src.common import textfile_read
from src.csv import csv_file_reader, csv_reader
from src.table import CsvFileTypeInfo, Table


@dataclass
class CsvReportInfo:
    """!
    @brief CSVファイルの情報
    """

    file_path: str
    csv_type_name: Optional[str] = None
    header_row_count: Optional[int] = None
    column_count_min: int = 0
    column_count_max: int = 0
    row_count: int = 0


def values_equal_index_group(values1: list[str], values2: list[str], index_list: list[int]) -> bool:
    """!
    @brief 文字列のリスト1とリスト2でインデックスリストの値が等しいか判定する
    @param values1 文字列のリスト1
    @param values2 文字列のリスト2
    @param index_list インデックスリスト
    @retval True 等しい
    @retval False 等しくない
    """
    for index in index_list:
        if values1[index] != values2[index]:
            return False
    return True


def values_non_empty(values: list[str], check_list: list[int]) -> list[int]:
    """!
    @brief 文字列のリストとインデックスのリストから値の入っているインデックスのリストを作成する
    @param values 文字列のリスト
    @param check_list 判定するインデックスのリスト
    @return 空以外のインデックスのリスト
    """
    index_list = []
    for index in check_list:
        if len(values) <= index:
            continue
        if values[index] != "":
            index_list.append(index)
    return index_list


def values_non_empty_index_group(values: list[str], index_group: list[list[int]]) -> list[int]:
    """!
    @brief 文字列のリストとインデックスグループのリストから値の入っているインデックスグループのリストを作成する
    @param values 文字列のリスト
    @param index_group インデックスリストのリスト
    @return 値の入っている。インデックスグループのリスト
    """
    result = []
    for i, check_list in enumerate(index_group):
        index_list = values_non_empty(values, check_list)
        if len(index_list) > 0:
            result.append(i)
    return result


def values_set_empty(values: list[str], index_list: list[int]):
    """!
    @brief 文字列のリストとインデックスのリストから値を空にする
    @param values 文字列のリスト
    @param index_list 判定するインデックスのリスト
    """
    for index in index_list:
        if len(values) <= index:
            continue
        values[index] = ""


def values_set_empty_index_group(values: list[str], index_group: list[list[int]]):
    """!
    @brief 文字列のリストとインデックスグループのリストから値を空にする
    @param values 文字列のリスト
    @param index_group インデックスリストのリスト
    """
    for check_list in index_group:
        values_set_empty(values, check_list)


def column_exclusive_index_group(table: Table, column_group: list[list[int]]):
    """!
    @brief カラムグループに従い、排他されるようにレコードを追加する
    @details 排他するカラムが同一レコードに存在する場合、そのレコードは複製して、排他するカラムを空にする
    """
    for row_index in itertools.count():  # 行を複製するため行が増えていく
        if row_index >= table.row_count():
            break
        columns = table._rows[row_index]
        index_group = values_non_empty_index_group(columns, column_group)
        if len(index_group) >= 2:  # 2つ以上のカラムグループに値が入っている。よって分離する必要がある
            duplicated_row = table.row_duplicate(row_index)
            # 元の行は、1つ目のカラムグループ以外のカラムを空にする
            empty_index_group = [column_group[i] for i in index_group[1:]]
            values_set_empty_index_group(columns, empty_index_group)
            # 複製した行は、1つ目のカラムグループを空にする
            values_set_empty(duplicated_row, column_group[index_group[0]])
    pass


def check_row_if(v_left: str, operator: str, v_right: str, *, row_if: Optional[str] = None) -> bool:
    """!
    @brief fillの実行を判定する
    @param v_left 左辺値
    @param operator 比較演算子
    @param v_right 右辺値
    @retval True 実行する
    @retval False 実行しない
    """
    if operator == "!=":
        if v_left != v_right:
            return True
    elif operator == "==":
        if v_left == v_right:
            return True
    else:
        raise Exception(f"--row-ifの指定が正しくありません。未サポート演算子。--raw-if {row_if}")
    return False


#


def column_fill_index(
    table: Table, column_index: int, value: str, *, ffill: bool = False, header: int = 0, row_if: Optional[str] = None
):
    """!
    @brief カラムの空白を埋める
    @param table テーブル
    @param column_index カラムのインデックス
    @param value 埋める文字列
    @param ffill 前方から埋める場合はTrue
    @param header ヘッダ行数
    @param row_if 置換を実行するかを行のカラムの値で判定
    """
    # row_ifのセットアップ
    if row_if is not None:
        match = re.match(r"(\d+)([!=><]=?)(.*)", row_if)
        if match is None:
            raise Exception(f"--row-ifの指定が正しくありません。--raw-if {row_if}")
        row_if_index = int(match.group(1))  # 先頭の数字部分
        row_if_operator = match.group(2)  # 比較演算子
        row_if_rest = match.group(3)  # 残りの文字列
        # 指定値の正規化
        row_if_index = int(row_if_index)
        ## 右辺の正規化
        match = re.search(r'(["\'])(.*?)\1', row_if_rest)
        if match:
            row_if_rest = match.group(2)  # クォート内の文字列を取得
    #
    value_prev = value
    for row in table._rows[header:]:
        column_value = row[column_index]
        if column_value == "":
            if row_if is not None:
                v_left = row[row_if_index]
                if check_row_if(v_left, row_if_operator, row_if_rest, row_if=row_if) == False:
                    continue
            if ffill:
                row[column_index] = value_prev
            else:
                row[column_index] = value
        else:
            value_prev = column_value
    pass


def column_merge_index_group(table: Table, column_key: list[int], column_group: list[list[int]]):
    """!
    @brief カラムグループに従い、排他されたレコードをマージする
    @param column_key マージする際にキーとするカラムのインデックス
    @param column_group カラムグループ
    """
    # column_keyとcolumn_group以外のカラムのインデックスリストを作成する
    other_column_index_list = {i for i in range(table.column_count())}
    other_column_index_list = other_column_index_list.difference(set(column_key))
    for column_index_list in column_group:
        other_column_index_list = other_column_index_list.difference(set(column_index_list))
    #
    row_index = 0
    # for row_index in itertools.count():  # 行をマージするため行が減っていく
    while True:  # 行をマージするため行が減っていく
        if (row_index + 1) >= table.row_count():  # 次の行が無くなったら終了
            break
        # 同一のキーを持つ行を探す
        columns1 = table._rows[row_index]
        columns2 = table._rows[row_index + 1]
        b = values_equal_index_group(columns1, columns2, column_key)
        if b == False:
            row_index += 1
            continue
        #
        # index_group1 = values_non_empty_index_group(columns1, column_group)
        index_group1 = set(values_non_empty_index_group(columns1, column_group))  # setにすることで、重複を除去する
        # index_group2 = values_non_empty_index_group(columns2, column_group)
        index_group2 = set(values_non_empty_index_group(columns2, column_group))  # setにすることで、重複を除去する
        if index_group1.isdisjoint(index_group2) == False:  # 重複があるためマージできない
            row_index += 1
            continue
        # column_keyとcolumn_group以外のカラムが同一であることを確認する
        b = values_equal_index_group(columns1, columns2, list(other_column_index_list))
        if b == False:
            row_index += 1
            continue
        # マージする
        for i in index_group2:
            for j in column_group[i]:
                table._rows[row_index][j] = columns2[j]
        # マージした行を削除する
        table.row_remove(row_index + 1)
    pass


def column_quote(table: Table, column_index: int) -> None:
    """!
    @brief カラムを空白で囲む
    @param table テーブル
    @param column_index カラムのインデックス
    """
    for row in table._rows:
        column_value = row[column_index]
        if len(column_value) > 1 and column_value[0] == '"':  # 既にクォートで囲んでいる?
            pass
        else:
            row[column_index] = f'"{column_value}"'


def csv_filetype_detect(csv_type_list: list[CsvFileTypeInfo], file_path: Path) -> Optional[CsvFileTypeInfo]:
    """!
    @brief CSVファイルの種別を判定する
    @param csv_type_list CSVファイルの種別のリスト
    @param file_path CSVファイルのパス
    @retval CSVファイルの種別
    @retval None 判定できない
    """
    # ファイルの読み込み
    lines = textfile_read(file_path, line_max=csv_type_list[0].header_row_count)
    # ファイルの種別判定
    return csv_filetype_detect_lines(csv_type_list, lines)


def csv_filetype_detect_lines(csv_type_list: list[CsvFileTypeInfo], lines: list[str]) -> Optional[CsvFileTypeInfo]:
    """!
    @brief CSVファイルの種別を判定する
    @param csv_type_list CSVファイルの種別のリスト
    @param lines 判定するヘッダ行※改行コードを含むこと
    @retval CSVファイルの種別
    @retval None 判定できない
    """
    # ファイルの種別判定
    for csv_type in csv_type_list:
        header_lines = csv_type.header_lines
        if lines[0 : len(header_lines)] == header_lines:
            return csv_type
    return None


def csv_filetype_list_read(csv_info_dir_path: Path) -> list[CsvFileTypeInfo]:
    """!
    @brief CSVファイルの種別を読み込む
    @param csv_info_dir_path CSV情報ファイルのディレクトリ
    @return CSVファイルの種別のリスト。ヘッダ行の長い順にソートされている。
    """
    # CSV種別のリストを作成
    csv_type_list: list[CsvFileTypeInfo] = []
    for file_path in csv_info_dir_path.glob("*_header.csv"):
        csv_type = csv_filetype_read(file_path)
        csv_type_list.append(csv_type)
    # CSV種別のリストをヘッダ行の長い順にソート※1行目が同一の場合に間違って判定しないようにするため
    csv_type_list.sort(key=lambda x: x.header_row_count, reverse=True)
    return csv_type_list


def csv_filetype_read(csv_info_path: Path) -> CsvFileTypeInfo:
    """!
    @brief CSVファイルの種別を読み込む
    @param csv_info_path CSV情報ファイル
    @return CSVファイルの種別
    """
    lines = textfile_read(csv_info_path)
    #
    type_name = ""
    if csv_info_path.name.endswith("_header.csv"):
        type_name = csv_info_path.name[: -len("_header.csv")]
    else:
        type_name = csv_info_path.stem
    #
    tbl = csv_reader(io.StringIO("".join(lines)))
    column_count = len(tbl._rows[0])
    row_count = tbl.row_count()
    #
    csv_type = CsvFileTypeInfo(
        type_name=type_name,
        header_lines=lines,
        header_column_count=column_count,
        header_row_count=row_count,
        _header_rows=tbl._rows,
    )
    return csv_type


def table_report(csv_type_list: list[CsvFileTypeInfo], file_path: Path) -> CsvReportInfo:
    """!
    @brief CSVファイルの情報を表示する
    """
    #
    csv_type_name: Optional[str] = None
    header_row_count = None
    csv_type = csv_filetype_detect(csv_type_list, file_path)
    if csv_type is not None:
        csv_type_name = csv_type.type_name
        header_row_count = csv_type.header_row_count
    #
    tbl = csv_file_reader(file_path)
    column_count_min = sys.maxsize
    column_count_max = -1
    row_count = tbl.row_count()
    for columns in tbl._rows:
        column_count = len(columns)
        column_count_min = min(column_count_min, column_count)
        column_count_max = max(column_count_max, column_count)
    # ファイルの情報を登録
    report_info = CsvReportInfo(
        file_path=file_path.as_posix(),
        csv_type_name=csv_type_name,
        header_row_count=header_row_count,
        column_count_min=column_count_min,
        column_count_max=column_count_max,
        row_count=row_count,
    )
    return report_info


def table_sort(table: Table, column_key_set: set[int], column_attr: list[str], *, reverse: bool = False):
    """!
    @brief テーブルをソートする
    @param table テーブル
    @param column_key_set ソートするカラムのインデックスのセット
    @param column_attr カラムの属性のリスト。str, int, float
    @param reverse 降順にする場合はTrue
    """

    # 複数の列でソートするラムダ関数
    def custom_sort(row):
        # return tuple(row[col] for col in column_key_set)
        result = []
        for i, col in enumerate(column_key_set):
            if column_attr[i] == "str":
                result.append(row[col])
            elif column_attr[i] == "int":
                result.append(int(row[col]))
            elif column_attr[i] == "float":
                result.append(float(row[col]))
            else:
                raise Exception("unknown column attribute")
        return tuple(result)

    #
    _sorted_data = sorted(table._rows, key=custom_sort, reverse=reverse)
    table._rows = _sorted_data
    pass
