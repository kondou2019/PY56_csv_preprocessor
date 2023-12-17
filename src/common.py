import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, cast


def textfile_read(
    file_path: Optional[Path], *, line_max: Optional[int] = None, remove_newline: bool = False, skip_line_count: int = 0
) -> list[str]:
    """!
    @brief テキストファイルを読み込む
    @details textfile_read_stream()のラッパー
    @param file_path テキストファイルのパス。Noneの場合は標準入力から読み込む。
    """
    if file_path is None:
        stream = TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        return textfile_read_stream(stream, skip_line_count=skip_line_count, line_max=line_max)
    #
    with open(file_path, mode="r", encoding="utf-8") as f:
        return textfile_read_stream(f, skip_line_count=skip_line_count, line_max=line_max)


def textfile_read_stream(
    i_stream: TextIOWrapper, *, line_max: Optional[int] = None, remove_newline: bool = False, skip_line_count: int = 0
) -> list[str]:
    """!
    @brief テキストファイルを読み込む
    @param i_stream 入力ストリーム
    @param line_max 読み込む最大行数。Noneの場合はすべて読み込む。
    @param remove_newline 改行を削除する
    @param skip_line_count 読み込みをスキップする行数
    @return テキストファイルの内容
    """
    lines: list[str] = []
    if line_max is None:
        # line_maxが指定されていない場合
        lines = i_stream.readlines()
        if skip_line_count > 0:
            lines = lines[skip_line_count:]
        if remove_newline:
            lines = [line.rstrip("\n") for line in lines]
    else:
        # line_maxが指定されている場合
        for _ in range(skip_line_count + line_max):
            line = i_stream.readline()
            if line == "":
                break
            if skip_line_count > 0:
                skip_line_count -= 1
                continue
            if remove_newline:
                line = line.rstrip("\n")
            lines.append(line)
    return lines


def textfile_write(
    file_path: Optional[Path],
    lines: list[str],
    *,
    append: bool = False,
    add_newline: bool = False,
    skip_line_count: int = 0
):
    """!
    @brief テキストファイルを出力
    @details textfile_write_stream()のラッパー
    @param file_path テキストファイルのパス。Noneの場合は標準出力に出力する。
    @param append 追記する
    """
    if file_path is None:
        stream = TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        return textfile_write_stream(stream, lines, add_newline=add_newline, skip_line_count=skip_line_count)
    #
    mode = "a" if append else "w"
    with open(file_path, mode=mode, encoding="utf-8") as f:
        stream = cast(TextIOWrapper, f)
        return textfile_write_stream(stream, lines, add_newline=add_newline, skip_line_count=skip_line_count)


def textfile_write_stream(
    o_stream: TextIOWrapper, lines: list[str], *, add_newline: bool = False, skip_line_count: int = 0
):
    """!
    @brief テキストファイルを出力
    @param o_stream 出力ストリーム
    @param lines 出力する内容
    @param add_newline 改行を追加する
    @param skip_line_count linesをスキップする行数
    """
    for line in lines:
        if skip_line_count > 0:
            skip_line_count -= 1
            continue
        if add_newline:
            line += "\n"
        o_stream.write(line)
    return
