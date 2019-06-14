import sys
from argparse import ArgumentParser, BooleanOptionalAction, Namespace

from sudoku_solver import __version__

sys.tracebacklimit = 0


def parse_args() -> Namespace:
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
        help="print a timing report",
    )
    parser.add_argument(
        "--show-timings",
        action=BooleanOptionalAction,
        help="print a timing report",
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

    return args
