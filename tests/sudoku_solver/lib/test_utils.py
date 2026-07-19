import pytest

from sudoku_solver.lib.exceptions import InvalidSudokuError, InvalidSudokuWarning
from sudoku_solver.lib.utils import cleanup_puzzle


def test_cleanup_puzzle() -> None:
    assert cleanup_puzzle("0" * 81) == "." * 81


def test_cleanup_invalid_puzzle() -> None:
    with pytest.warns(InvalidSudokuWarning, match="Invalid sudoku: invalid"):
        assert cleanup_puzzle("invalid") == ""


def test_cleanup_invalid_puzzle_strict() -> None:
    with pytest.raises(InvalidSudokuError, match="Invalid sudoku: invalid"):
        cleanup_puzzle("invalid", strict=True)
