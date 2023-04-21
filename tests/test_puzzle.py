import pytest

from sudoku_solver.puzzle import SudokuPuzzle

from tests.data.sudoku import puzzles


@pytest.mark.parametrize(
    ("sudoku", "solution"),
    [(puzzle["puzzle"], puzzle["solution"]) for puzzle in puzzles],
)
def test_sudoku(sudoku: str, solution: str) -> None:
    puzzle = SudokuPuzzle(sudoku)
    puzzle.solve()
    assert str(puzzle) == solution
