def _exception_message(sudoku: str) -> str:
    return f"Invalid sudoku: {sudoku}"


class InvalidSudokuError(RuntimeError):
    def __init__(self, sudoku: str) -> None:
        super().__init__(_exception_message(sudoku))


class InvalidSudokuWarning(RuntimeWarning):
    @staticmethod
    def message(sudoku: str) -> str:
        return _exception_message(sudoku)
