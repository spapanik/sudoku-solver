from unittest import mock

import pytest
from pyutilkit.term import SGRCodes, SGROutput, SGRString

from sudoku_solver.lib.puzzle import SudokuPuzzle

from tests.helpers import get_sudoku_puzzles


@pytest.mark.parametrize(
    ("sudoku", "solution"),
    [(puzzle["puzzle"], puzzle["solution"]) for puzzle in get_sudoku_puzzles()],
)
def test_sudoku(sudoku: str, solution: str) -> None:
    puzzle = SudokuPuzzle(sudoku)
    puzzle.solve()
    assert str(puzzle) == solution


def test_format() -> None:
    sudoku = "123456789" * 9
    puzzle = SudokuPuzzle(sudoku)
    row = "│1 2 3│4 5 6│7 8 9│"
    expected = (
        f"{puzzle.top}\n"
        f"{row}\n"
        f"{row}\n"
        f"{row}\n"
        f"{puzzle.mid}\n"
        f"{row}\n"
        f"{row}\n"
        f"{row}\n"
        f"{puzzle.mid}\n"
        f"{row}\n"
        f"{row}\n"
        f"{row}\n"
        f"{puzzle.bottom}\n"
    )

    assert repr(puzzle) == f"SudokuPuzzle({sudoku})"
    assert puzzle.matrix == expected
    assert puzzle.format(pretty=False) == SGROutput([sudoku])
    assert puzzle.format(pretty=True) == SGROutput([expected])


def test_format_highlight() -> None:
    sudoku = "123456789" * 9
    puzzle = SudokuPuzzle(sudoku)

    assert puzzle.format(pretty=False, highlight={1}) == SGROutput(
        [
            SGRString("1"),
            SGRString("2", params=[SGRCodes.GREEN]),
            SGRString(sudoku[2:]),
        ]
    )
    assert puzzle.format(pretty=True, highlight={1}) == SGROutput(
        [
            SGRString(f"{puzzle.top}\n│1 "),
            SGRString("2", params=[SGRCodes.GREEN]),
            SGRString(puzzle.matrix[len(puzzle.top) + 5 :]),
        ]
    )


def test_calculated_and_last_step() -> None:
    sudoku_info = get_sudoku_puzzles()[0]
    puzzle = SudokuPuzzle(sudoku_info["puzzle"])
    missing = {index for index, cell in enumerate(sudoku_info["puzzle"]) if cell == "."}

    assert puzzle.calculated == set()

    puzzle.step()

    assert puzzle.last_step == puzzle.calculated
    assert puzzle.calculated <= missing

    puzzle.solve()

    assert puzzle.calculated == missing
    assert puzzle.last_step < missing


def test_debug_info() -> None:
    sudoku = "." + "1" * 79 + "."
    puzzle = SudokuPuzzle(sudoku)
    puzzle.candidates[0] = set()

    assert puzzle.debug_info == (
        f"cells: {sudoku}\n"
        "candidates: {\n"
        "\tA1(00): no candidates,\n"
        "\tI9(80): {2, 3, 4, 5, 6, 7, 8, 9, \b\b},\n"
        "}\n"
    )


@mock.patch.object(SudokuPuzzle, "step", return_value=None)
def test_no_solution(mock_step: mock.MagicMock) -> None:
    puzzle = SudokuPuzzle("." + "1" * 80)

    assert puzzle.solve() is False
    mock_step.assert_called_once_with()


@mock.patch.object(SudokuPuzzle, "_hidden_single", return_value=True)
@mock.patch.object(SudokuPuzzle, "_naked_single", return_value=False)
def test_step_reports_technique(
    mock_naked_single: mock.MagicMock, mock_hidden_single: mock.MagicMock
) -> None:
    puzzle = SudokuPuzzle("." + "1" * 80)

    assert puzzle.step() == "hidden single"
    mock_naked_single.assert_called_once_with()
    mock_hidden_single.assert_called_once_with()


def test_step_on_stuck_puzzle() -> None:
    puzzle = SudokuPuzzle("." + "1" * 80)
    puzzle.candidates[0] = set()

    assert puzzle.step() is None


def test_x_wing_in_rows() -> None:
    puzzle = SudokuPuzzle("1" * 81)
    puzzle.candidates = {
        0: {"1"},
        1: {"1"},
        2: {"1"},
        9: {"1"},
        10: {"1"},
    }

    assert puzzle._x_wing_for_cells(0, 10) is True
    assert puzzle.candidates[2] == set()
