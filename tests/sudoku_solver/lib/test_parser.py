from unittest import mock

import pytest

from sudoku_solver.lib.parser import parse_args


@pytest.mark.parametrize(
    ("verbose", "expected_verbosity"),
    [("-v", 1), ("-vv", 2), ("-vvvvv", 5)],
)
def test_sudoku_solver_verbose(verbose: str, expected_verbosity: int) -> None:
    with mock.patch("sys.argv", ["solve", verbose, "."]):
        args = parse_args()

    assert args.verbosity == expected_verbosity


def test_sudoku_solver_defaults() -> None:
    with mock.patch("sys.argv", ["solve", "."]):
        args = parse_args()

    assert args.verbosity == 0
    assert args.shortcircuit is False
    assert args.show_timings is False
    assert args.strict is False
    assert args.pretty is False
    assert args.step_by_step is False


@pytest.mark.parametrize(
    ("flag", "expected"),
    [("--step-by-step", True), ("--no-step-by-step", False)],
)
def test_sudoku_solver_step_by_step(flag: str, expected: bool) -> None:
    with mock.patch("sys.argv", ["solve", flag, "."]):
        args = parse_args()

    assert args.step_by_step is expected
