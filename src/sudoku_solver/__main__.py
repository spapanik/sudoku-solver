from sudoku_solver.command.solve import SolveCommand
from sudoku_solver.lib.parser import parse_args


def main() -> None:
    args = parse_args()
    SolveCommand(
        *args.puzzles,
        shortcircuit=args.shortcircuit,
        show_timings=args.show_timings,
        strict=args.strict,
        pretty=args.pretty,
    ).solve()
