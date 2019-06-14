import os

from pyutilkit.term import SGRCodes, SGROutput, SGRString
from pyutilkit.timing import Stopwatch

from sudoku_solver.lib.puzzle import SudokuPuzzle
from sudoku_solver.lib.utils import cleanup_puzzle


class SolveCommand:
    __slots__ = ("pretty", "shortcircuit", "show_timings", "sudokus", "timings")

    def __init__(
        self,
        *sudokus: str,
        shortcircuit: bool,
        show_timings: bool,
        strict: bool,
        pretty: bool,
    ) -> None:
        self.shortcircuit = shortcircuit
        self.show_timings = show_timings
        self.sudokus = [
            SudokuPuzzle(clean_sudoku)
            for sudoku in sudokus
            if (clean_sudoku := cleanup_puzzle(sudoku, strict=strict))
        ]
        self.pretty = pretty
        self.timings = Stopwatch()

    def solve(self) -> None:
        for sudoku in self.sudokus:
            SGROutput(
                [
                    SGRString("🔍 Solving sudoku:", params=[SGRCodes.BLUE]),
                    sudoku.format(pretty=self.pretty),
                ]
            ).print(sep=os.linesep)
            with self.timings:
                success = sudoku.solve()
            if success:
                SGROutput(
                    [
                        SGRString("🎉 Solution:", params=[SGRCodes.GREEN]),
                        sudoku.format(pretty=self.pretty),
                    ]
                ).print(sep=os.linesep, end=os.linesep * 2)
            else:
                SGROutput(
                    [
                        SGRString("💔 No solution found!", params=[SGRCodes.RED]),
                        SGRString("Last step:", params=[SGRCodes.RED]),
                        sudoku.format(pretty=self.pretty),
                    ]
                ).print(sep=os.linesep, end=os.linesep * 2)
                if self.shortcircuit:
                    break

        if self.show_timings:
            SGRString(f"🧮 Total time: {self.timings.elapsed}").print()
            SGRString(f"📊 Average time: {self.timings.average}").print()
