# import pytest
import io

from src.common import textfile_read_stream

LINE_3 = """\
line1
line2
line3
"""


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
