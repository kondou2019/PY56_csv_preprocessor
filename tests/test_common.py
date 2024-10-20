import io

import pytest

from src.common import split_csv_string_no_normalize, textfile_read_stream

LINE_3 = """\
line1
line2
line3
"""


@pytest.mark.parametrize(
    "test_id, val, expected",
    [
        ("0101N", "a,b", ["a", "b"]),
        ("0102N", "a,,c", ["a", "", "c"]),  # 空文字
        ("0103N", "a, ,c", ["a", " ", "c"]),  # スペース
        ("0104N", " a , b ", [" a ", " b "]),  # 前後のスペース
        ("0201B", "a", ["a"]),
        ("0202B", "", []),
        ("0203B", " ", [" "]),  # スペース
        ("0204N", "a,", ["a", ""]),  # 最後に値なし
        ("0205N", "a, ", ["a", " "]),  # 最後に空白
        ("0301N", 'a,"b1,b2"', ["a", '"b1,b2"']),
        ("0302N", 'a,"b1,"",b2"', ["a", '"b1,"",b2"']),  # ダブルクォートのエスケープ
        ("0303B", 'a,"b1,b2', ["a", '"b1,b2']),  # 閉じるダブルクォートが無い
    ],
)
def test_split_csv_string_no_normalize_0001X(test_id: str, val: str, expected: list[str]):
    result = split_csv_string_no_normalize(val)
    assert result == expected


@pytest.mark.parametrize(
    "test_id, val, expected",
    [
        ("0101N", "a\tb", ["a", "b"]),
        ("0201N", 'a\t"b1,b2"', ["a", '"b1,b2"']),
    ],
)
def test_split_csv_string_no_normalize_0002X(test_id: str, val: str, expected: list[str]):  # 区切り記号
    result = split_csv_string_no_normalize(val, delimiter="\t")
    assert result == expected


@pytest.mark.parametrize(
    "test_id, val, expected",
    [
        ("0101N", "a,b", ["a", "b"]),  # スペースなし
        ("0201N", " a, b", ["a", "b"]),  # 前後にスペース
    ],
)
def test_split_csv_string_no_normalize_0003X(test_id: str, val: str, expected: list[str]):  # strip=True
    result = split_csv_string_no_normalize(val, strip=True)
    assert result == expected


def test_textfile_read_stream_0101N():
    lines = textfile_read_stream(io.StringIO(LINE_3))
    assert lines == ["line1\n", "line2\n", "line3\n"]


def test_textfile_read_stream_0102B():
    lines = textfile_read_stream(io.StringIO(LINE_3), line_max=2)
    assert lines == ["line1\n", "line2\n"]


def test_textfile_read_stream_0103B():
    lines = textfile_read_stream(io.StringIO(LINE_3), skip_line_count=1)
    assert lines == ["line2\n", "line3\n"]


def test_textfile_read_stream_0104B():  # skip_line_count,line_maxを同時に指定
    lines = textfile_read_stream(io.StringIO(LINE_3), skip_line_count=1, line_max=1)
    assert lines == ["line2\n"]


def test_textfile_read_stream_0105N():  # remove_newline
    lines = textfile_read_stream(io.StringIO(LINE_3), remove_newline=True)
    assert lines == ["line1", "line2", "line3"]


def test_textfile_read_stream_0106B():  # skip_line_count,line_max,remove_newlineを同時に指定
    lines = textfile_read_stream(io.StringIO(LINE_3), skip_line_count=1, line_max=1, remove_newline=True)
    assert lines == ["line2"]
