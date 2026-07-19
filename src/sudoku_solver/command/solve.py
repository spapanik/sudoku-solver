import os

from pyutilkit.term import SGRCodes, SGROutput, SGRString
from pyutilkit.timing import Stopwatch

from sudoku_solver.lib.puzzle import SudokuPuzzle
from sudoku_solver.lib.utils import cleanup_puzzle


class SolveCommand:
    __slots__ = (
        "pretty",
        "shortcircuit",
        "show_timings",
        "step_by_step",
        "sudokus",
        "timings",
    )

    def __init__(
        self,
        *sudokus: str,
        shortcircuit: bool,
        show_timings: bool,
        strict: bool,
        pretty: bool,
        step_by_step: bool = False,
    ) -> None:
        self.shortcircuit = shortcircuit
        self.show_timings = show_timings
        self.sudokus = [
            SudokuPuzzle(clean_sudoku)
            for sudoku in sudokus
            if (clean_sudoku := cleanup_puzzle(sudoku, strict=strict))
        ]
        self.pretty = pretty
        self.step_by_step = step_by_step
        self.timings = Stopwatch()

    def solve(self) -> None:
        for sudoku in self.sudokus:
            SGRString("🔍 Solving sudoku:", params=[SGRCodes.BLUE]).print()
            sudoku.format(pretty=self.pretty).print()
            success = self._solve(sudoku)
            if success is None:
                SGRString("⏸️ Solving paused!", params=[SGRCodes.YELLOW]).print(
                    end=os.linesep * 2
                )
                break
            if success:
                SGRString("🎉 Solution:", params=[SGRCodes.GREEN]).print()
                sudoku.format(pretty=self.pretty, highlight=sudoku.calculated).print(
                    end=os.linesep * 2
                )
            else:
                SGROutput(
                    [
                        SGRString("💔 No solution found!", params=[SGRCodes.RED]),
                        SGRString("Last step:", params=[SGRCodes.RED]),
                    ]
                ).print(sep=os.linesep)
                sudoku.format(pretty=self.pretty).print(end=os.linesep * 2)
                if self.shortcircuit:
                    break

        if self.show_timings:
            SGRString(f"🧮 Total time: {self.timings.elapsed}").print()
            SGRString(f"📊 Average time: {self.timings.average}").print()

    def _solve(self, sudoku: SudokuPuzzle) -> bool | None:
        if not self.step_by_step:
            with self.timings:
                return sudoku.solve()
        return self._solve_step_by_step(sudoku)

    def _solve_step_by_step(self, sudoku: SudokuPuzzle) -> bool | None:
        """Solve one step at a time, pausing for confirmation between steps.

        Return True if solved, False if stuck, or None if the user stopped.
        """
        while not sudoku.is_solved:
            with self.timings:
                method = sudoku.step()
            if method is None:
                return False
            SGRString(f"🧩 Technique used: {method}", params=[SGRCodes.CYAN]).print()
            sudoku.format(pretty=self.pretty, highlight=sudoku.last_step).print()
            if not sudoku.is_solved and not self._prompt_continue():
                return None
        return True

    @staticmethod
    def _prompt_continue() -> bool:
        return input("continue Y/n: ").strip().lower() not in {"n", "no"}
