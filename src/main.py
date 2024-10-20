#!/usr/bin/env python3

import click

from src.cmd_column import (
    cmd_column_add,
    cmd_column_del,
    cmd_column_exclusive,
    cmd_column_fill,
    cmd_column_merge,
    cmd_column_move,
    cmd_column_quote,
    cmd_column_replace,
    cmd_column_select,
    cmd_column_sort,
)
from src.cmd_csv import cmd_csv_filetype, cmd_csv_header_add, cmd_csv_header_change, cmd_csv_header_del, cmd_csv_report

__VERSION__ = "0.5.255"


# サブコマンドをメインコマンドに追加
@click.group(help="CSVファイルの前処理ツール")
@click.version_option(version=__VERSION__)
def cli():
    pass


cli.add_command(cmd_column_add)
cli.add_command(cmd_column_del)
cli.add_command(cmd_column_exclusive)
cli.add_command(cmd_column_fill)
cli.add_command(cmd_column_merge)
cli.add_command(cmd_column_move)
cli.add_command(cmd_column_quote)
cli.add_command(cmd_column_replace)
cli.add_command(cmd_column_select)
cli.add_command(cmd_column_sort)
cli.add_command(cmd_csv_filetype)
cli.add_command(cmd_csv_header_add)
cli.add_command(cmd_csv_header_change)
cli.add_command(cmd_csv_header_del)
cli.add_command(cmd_csv_report)


def main(argv: list[str]) -> int:
    """!
    @brief 主入口点
    @param argv コマンドラインオプション
    @retval 0 成功
    @retval 1 失敗
    """
    cli(standalone_mode=False)


# if __name__ == "__main__":
#    sys.exit(main(sys.argv))
