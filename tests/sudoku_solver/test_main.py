from unittest import mock

from sudoku_solver.__main__ import main
from sudoku_solver.command.solve import SolveCommand

from tests.helpers import get_sudoku_puzzles

VALID_PUZZLES = [sudoku["puzzle"] for sudoku in get_sudoku_puzzles()]


@mock.patch(
    "sudoku_solver.__main__.parse_args",
    new=mock.MagicMock(return_value=mock.MagicMock(puzzles=VALID_PUZZLES)),
)
@mock.patch.object(SolveCommand, "solve")
def test_clone(mock_solve: mock.MagicMock) -> None:
    main()
    assert mock_solve.call_count == 1
    calls = [mock.call()]
    assert mock_solve.call_args_list == calls


@mock.patch(
    "sudoku_solver.__main__.parse_args",
    new=mock.MagicMock(return_value=mock.MagicMock(puzzles=VALID_PUZZLES)),
)
@mock.patch.object(SolveCommand, "solve")
def test_generate(mock_solve: mock.MagicMock) -> None:
    main()
    assert mock_solve.call_count == 1
    calls = [mock.call()]
    assert mock_solve.call_args_list == calls
