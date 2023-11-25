# import pytest
import io

from tests.tool_csv import generate_alphabet_base26


def test_generate_alphabet_base26():
    result = generate_alphabet_base26(1)
    assert result == "A"
    result = generate_alphabet_base26(2)
    assert result == "B"
    result = generate_alphabet_base26(27)
    assert result == "AA"
    pass
