import pytest

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
