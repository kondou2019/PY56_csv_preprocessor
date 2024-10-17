import io

import pytest

from src.table_utl import check_row_if


@pytest.mark.parametrize(
    "test_id, v_left, operator, v_right, expected",
    [
        ("0101N", "", "!=", "", False),
        ("0101N", "", "==", "", True),
    ],
)
def test_check_row_if_0001X(test_id: str, v_left: str, operator: str, v_right: str, expected: bool) -> None:
    """!
    @brief テストケース
    @param[in] test_id テスト識別子
    @param[in] val 入力値
    @param[in] expected 期待値
    """
    result = check_row_if("", "!=", "")
    assert result == False
