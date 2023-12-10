import itertools
from typing import Optional

from src.table import Table


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


def column_fill_index(table: Table, column_index: int, value: str, *, ffill: bool = False):
    """!
    @brief カラムの空白を埋める
    @param table テーブル
    @param column_index カラムのインデックス
    @param value 埋める文字列
    @param ffill 前方から埋める場合はTrue
    """
    value_prev = value
    for row in table._rows:
        column_value = row[column_index]
        if column_value == "":
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
        index_group1 = values_non_empty_index_group(columns1, column_group)
        index_group1 = set(index_group1)  # setにすることで、重複を除去する
        index_group2 = values_non_empty_index_group(columns2, column_group)
        index_group2 = set(index_group2)  # setにすることで、重複を除去する
        if index_group1.isdisjoint(index_group2) == False:  # 重複があるためマージできない
            row_index += 1
            continue
        # column_keyとcolumn_group以外のカラムが同一であることを確認する
        b = values_equal_index_group(columns1, columns2, other_column_index_list)
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
