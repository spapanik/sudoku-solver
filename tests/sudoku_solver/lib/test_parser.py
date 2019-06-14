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
    assert args.shortcircuit is None
    assert args.show_timings is None
    assert args.strict is None
    assert args.pretty is None
