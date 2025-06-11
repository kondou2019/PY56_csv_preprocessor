import io
from typing import Optional

import pytest

from src.filter.multi_value.filter import MultiValueFilter, multi_value_join, multi_value_split

# from src.lib.csv import csv_reader
# from src.lib.table import Table


@pytest.mark.parametrize(
    "_test_id, val, kwargs, expected",
    [
        ("0101N", '"a,b"', {"regex": "^a$", "repl": "x"}, '"x,b"'),  # 置換
        ("0101N", '"1,2"', {"regex": "^a$", "repl": "x"}, '"1,2"'),  # 置換なし
        ("0102N", "a", {"regex": "^a$", "repl": "x"}, "x"),  # クォートなし,置換
        ("0103N", "1", {"regex": "^a$", "repl": "x"}, "1"),  # クォートなし,置換なし
        ("0104N", "", {"regex": "^a$", "repl": "x"}, ""),  # 空文字
        ("0105N", '"a,b"', {"regex": "^a$", "repl": ""}, '",b"'),  # 削除
        ("0201N", '"a,b,a"', {"regex": "^a$", "repl": "x"}, '"x,b"'),  # 重複
    ],
)
def test_filter_execute_cell(_test_id: str, val: str, kwargs: dict[str, Optional[str]], expected: str) -> None:
    filter = MultiValueFilter.new_filter()
    result = filter.filter_execute_cell(val, **kwargs)
    assert result == expected


@pytest.mark.parametrize(
    "_test_id, val, quote, expected",
    [
        ("0101N", ["a", "b"], True, '"a,b"'),
        ("0102N", ["a"], False, "a"),
    ],
)
def test_multi_value_join_0001X(_test_id: str, val: str, quote: bool, expected: tuple[list[str], bool]) -> None:
    result = multi_value_join(val, quote)
    assert result == expected


@pytest.mark.parametrize(
    "_test_id, val, expected",
    [
        ("0101N", '"a,b"', (["a", "b"], True)),
        ("0102N", "a", (["a"], False)),
    ],
)
def test_multi_value_split_0001X(_test_id: str, val: str, expected: tuple[list[str], bool]) -> None:
    result = multi_value_split(val)
    assert result == expected
