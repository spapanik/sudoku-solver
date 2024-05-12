import argparse
import sys
from time import perf_counter_ns

from pyutilkit.timing import Timing

from sudoku_solver import __version__
from sudoku_solver.puzzle import SudokuPuzzle
from sudoku_solver.utils import cleanup_puzzle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sudoku solver", description="Yet another sudoku solver"
    )

    # positional arguments
    parser.add_argument("puzzles", help="the sudoku puzzle", nargs="+")

    # optional arguments
    parser.add_argument(
        "-s",
        "--shortcircuit",
        action="store_true",
        help="if a puzzle cannot be solved, stop",
    )
    parser.add_argument(
        "-t",
        "--timings",
        action="store_true",
        help="print a timing report",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="print the version and exit",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timings = []
    for puzzle in args.puzzles:
        clean_puzzle = cleanup_puzzle(puzzle)
        if len(clean_puzzle) != 81:
            print("Invalid puzzle:", file=sys.stderr)
            print(clean_puzzle, file=sys.stderr)
            continue

        sudoku = SudokuPuzzle(clean_puzzle)
        start = perf_counter_ns()
        success = sudoku.solve()
        end = perf_counter_ns()
        timings.append(end - start)
        if success:
            print("Solved sudoku puzzle:")
            print(f"{sudoku.matrix}")
        else:
            print("Failed to solve sudoku:", file=sys.stderr)
            print(sudoku.matrix, file=sys.stderr)
            print("Debug info:", file=sys.stderr)
            print(sudoku.debug_info, file=sys.stderr)
            if args.shortcircuit:
                break

    if args.timings:
        if not timings:
            print("No timings to report", file=sys.stderr)
            return
        total_time = sum(timings)
        average_time = total_time // len(timings)
        print("Timings:")
        print(f"Total time: {Timing(nanoseconds=total_time)}")
        print(f"Average time: {Timing(nanoseconds=average_time)}")
