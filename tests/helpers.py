import json
from pathlib import Path
from typing import TypedDict, cast

DATA_PATH = Path(__file__).parent.joinpath("data", "sudoku.json")


class SudokuInfo(TypedDict):
    puzzle: str
    solution: str


def get_sudoku_puzzles() -> list[SudokuInfo]:
    return cast("list[SudokuInfo]", json.loads(DATA_PATH.read_text()))
