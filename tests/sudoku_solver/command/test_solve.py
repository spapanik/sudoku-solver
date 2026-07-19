import os
from unittest import mock

import pytest

from sudoku_solver.command.solve import SolveCommand

from tests.helpers import get_sudoku_puzzles


@mock.patch("sudoku_solver.command.solve.Stopwatch")
@mock.patch("sudoku_solver.command.solve.SudokuPuzzle")
@mock.patch("sudoku_solver.command.solve.cleanup_puzzle", side_effect=["clean", ""])
def test_init(
    mock_cleanup_puzzle: mock.MagicMock,
    mock_sudoku_puzzle: mock.MagicMock,
    mock_stopwatch: mock.MagicMock,
) -> None:
    command = SolveCommand(
        "valid",
        "invalid",
        shortcircuit=True,
        show_timings=True,
        strict=True,
        pretty=True,
    )

    assert command.shortcircuit is True
    assert command.show_timings is True
    assert command.pretty is True
    assert command.sudokus == [mock_sudoku_puzzle.return_value]
    assert command.timings == mock_stopwatch.return_value
    assert mock_cleanup_puzzle.call_args_list == [
        mock.call("valid", strict=True),
        mock.call("invalid", strict=True),
    ]
    mock_sudoku_puzzle.assert_called_once_with("clean")


@mock.patch("sudoku_solver.command.solve.SGRString")
@mock.patch("sudoku_solver.command.solve.SGROutput")
def test_solve(
    mock_sgr_output: mock.MagicMock, mock_sgr_string: mock.MagicMock
) -> None:
    sudoku = mock.MagicMock()
    sudoku.solve.return_value = True
    command = SolveCommand(
        shortcircuit=False, show_timings=True, strict=False, pretty=True
    )
    command.sudokus = [sudoku]
    command.timings = mock.MagicMock()

    command.solve()

    sudoku.solve.assert_called_once_with()
    assert sudoku.format.call_args_list == [
        mock.call(pretty=True),
        mock.call(pretty=True, highlight=sudoku.calculated),
    ]
    assert sudoku.format.return_value.print.call_count == 2
    mock_sgr_output.return_value.print.assert_not_called()
    assert mock_sgr_string.return_value.print.call_count == 4


@pytest.mark.parametrize(
    ("shortcircuit", "expected_call_count"),
    [(False, 2), (True, 1)],
)
@mock.patch("sudoku_solver.command.solve.SGRString")
@mock.patch("sudoku_solver.command.solve.SGROutput")
def test_no_solution(
    mock_sgr_output: mock.MagicMock,
    mock_sgr_string: mock.MagicMock,
    shortcircuit: bool,
    expected_call_count: int,
) -> None:
    sudokus = [mock.MagicMock(), mock.MagicMock()]
    for sudoku in sudokus:
        sudoku.solve.return_value = False
    command = SolveCommand(
        shortcircuit=shortcircuit,
        show_timings=False,
        strict=False,
        pretty=False,
    )
    command.sudokus = [sudokus[0], sudokus[1]]
    command.timings = mock.MagicMock()

    command.solve()

    assert sum(sudoku.solve.call_count for sudoku in sudokus) == expected_call_count
    assert mock_sgr_output.return_value.print.call_count == expected_call_count
    assert mock_sgr_string.return_value.print.call_count == expected_call_count


@mock.patch("builtins.input", return_value="")
@mock.patch("sudoku_solver.command.solve.SGRString", new=mock.MagicMock())
@mock.patch("sudoku_solver.command.solve.SGROutput", new=mock.MagicMock())
def test_solve_step_by_step(mock_input: mock.MagicMock) -> None:
    sudoku_info = get_sudoku_puzzles()[0]
    command = SolveCommand(
        sudoku_info["puzzle"],
        shortcircuit=False,
        show_timings=False,
        strict=False,
        pretty=False,
        step_by_step=True,
    )

    command.solve()

    assert str(command.sudokus[0]) == sudoku_info["solution"]
    assert mock_input.call_count > 0


@mock.patch("builtins.input", return_value="n")
@mock.patch("sudoku_solver.command.solve.SGRString", new=mock.MagicMock())
@mock.patch("sudoku_solver.command.solve.SGROutput", new=mock.MagicMock())
def test_solve_step_by_step_stopped(mock_input: mock.MagicMock) -> None:
    sudoku_info = get_sudoku_puzzles()[0]
    command = SolveCommand(
        sudoku_info["puzzle"],
        shortcircuit=False,
        show_timings=False,
        strict=False,
        pretty=False,
        step_by_step=True,
    )

    command.solve()

    assert not command.sudokus[0].is_solved
    mock_input.assert_called_once_with("continue Y/n: ")


@mock.patch("sudoku_solver.command.solve.SGRString")
@mock.patch("sudoku_solver.command.solve.SGROutput")
def test_solve_step_by_step_stuck(
    mock_sgr_output: mock.MagicMock, mock_sgr_string: mock.MagicMock
) -> None:
    sudoku = mock.MagicMock(is_solved=False)
    sudoku.step.return_value = None
    command = SolveCommand(
        shortcircuit=False,
        show_timings=False,
        strict=False,
        pretty=False,
        step_by_step=True,
    )
    command.sudokus = [sudoku]
    command.timings = mock.MagicMock()

    command.solve()

    sudoku.step.assert_called_once_with()
    mock_sgr_output.return_value.print.assert_called_once_with(sep=os.linesep)
    assert mock_sgr_string.return_value.print.call_count == 1
