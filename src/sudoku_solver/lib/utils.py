import re
from warnings import warn

from sudoku_solver.lib.constants import INVALID_CHARS
from sudoku_solver.lib.exceptions import InvalidSudokuError, InvalidSudokuWarning


def cleanup_puzzle(puzzle: str, *, strict: bool = False) -> str:
    clean_puzzle = re.sub(INVALID_CHARS, ".", puzzle)
    if len(clean_puzzle) != 81:  # noqa: PLR2004
        if strict:
            raise InvalidSudokuError(puzzle)
        warn(InvalidSudokuWarning.message(puzzle), InvalidSudokuWarning, stacklevel=3)
        return ""
    return clean_puzzle
