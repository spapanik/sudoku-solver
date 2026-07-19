from __future__ import annotations

import sys
from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sudoku_solver.__version__ import __version__

if TYPE_CHECKING:
    from typing import Self

sys.tracebacklimit = 0


@dataclass(frozen=True, slots=True)
class CliArgs:
    puzzles: list[str]
    strict: bool
    shortcircuit: bool
    pretty: bool
    show_timings: bool
    step_by_step: bool
    verbosity: int

    @classmethod
    def from_args(cls, args: Namespace, /) -> Self:
        return cls(
            puzzles=args.puzzles,
            strict=bool(args.strict),
            shortcircuit=bool(args.shortcircuit),
            pretty=bool(args.pretty),
            show_timings=bool(args.show_timings),
            step_by_step=bool(args.step_by_step),
            verbosity=args.verbosity,
        )


def parse_args() -> CliArgs:
    parser = ArgumentParser(
        prog="sudoku solver", description="Yet another sudoku solver"
    )

    # positional arguments
    parser.add_argument("puzzles", help="the sudoku puzzle", nargs="+")

    # optional arguments
    parser.add_argument(
        "--strict",
        action=BooleanOptionalAction,
        help="if a puzzle cannot be parsed, stop",
    )
    parser.add_argument(
        "--shortcircuit",
        action=BooleanOptionalAction,
        help="if a puzzle cannot be solved, stop",
    )
    parser.add_argument(
        "--pretty",
        action=BooleanOptionalAction,
        help="pretty print the puzzles",
    )
    parser.add_argument(
        "--show-timings",
        action=BooleanOptionalAction,
        help="print a timing report",
    )
    parser.add_argument(
        "--step-by-step",
        action=BooleanOptionalAction,
        help="solve one step at a time, printing the technique used",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="print the version and exit",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="increase the level of verbosity",
    )

    args = parser.parse_args()
    if args.verbosity > 0:
        sys.tracebacklimit = 1000

    return CliArgs.from_args(args)
