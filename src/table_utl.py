import itertools

from src.table import Table


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
