import itertools
import re
from dataclasses import dataclass

from pyutilkit.classes import Singleton

INVALID_CHARS = re.compile(r"[^1-9.]")


@dataclass(frozen=True, slots=True)
class SudokuConstants(metaclass=Singleton):
    digits: frozenset[str]
    rows: tuple[frozenset[int], ...]
    columns: tuple[frozenset[int], ...]
    boxes: tuple[frozenset[int], ...]
    indices_in_same_row: tuple[frozenset[int], ...]
    indices_in_same_column: tuple[frozenset[int], ...]
    indices_in_same_box: tuple[frozenset[int], ...]
    collisions: tuple[frozenset[int], ...]

    def __init__(self) -> None:
        digits: frozenset[str] = frozenset("123456789")
        rows: list[set[int]] = [set() for _ in range(9)]
        columns: list[set[int]] = [set() for _ in range(9)]
        boxes: list[set[int]] = [set() for _ in range(9)]
        indices_in_same_row: list[set[int]] = [set() for _ in range(81)]
        indices_in_same_column: list[set[int]] = [set() for _ in range(81)]
        indices_in_same_box: list[set[int]] = [set() for _ in range(81)]
        collisions: list[set[int]] = [set() for _ in range(81)]

        for i, j in itertools.product(range(9), range(9)):
            rows[i].add(9 * i + j)
            columns[i].add(9 * j + i)
            boxes[i].add(27 * (i // 3) + 3 * (i % 3) + j % 3 + 9 * (j // 3))

        for i in range(81):
            for j in range(i):
                if i // 9 == j // 9:
                    indices_in_same_row[i].add(j)
                    indices_in_same_row[j].add(i)
                    collisions[i].add(j)
                    collisions[j].add(i)
                if (i - j) % 9 == 0:
                    indices_in_same_column[i].add(j)
                    indices_in_same_column[j].add(i)
                    collisions[i].add(j)
                    collisions[j].add(i)
                if i // 27 == j // 27 and (i % 9) // 3 == (j % 9) // 3:
                    indices_in_same_box[i].add(j)
                    indices_in_same_box[j].add(i)
                    collisions[i].add(j)
                    collisions[j].add(i)

        object.__setattr__(self, "digits", digits)
        object.__setattr__(self, "rows", tuple(frozenset(row) for row in rows))
        object.__setattr__(
            self, "columns", tuple(frozenset(column) for column in columns)
        )
        object.__setattr__(self, "boxes", tuple(frozenset(box) for box in boxes))
        object.__setattr__(
            self,
            "indices_in_same_row",
            tuple(frozenset(index) for index in indices_in_same_row),
        )
        object.__setattr__(
            self,
            "indices_in_same_column",
            tuple(frozenset(index) for index in indices_in_same_column),
        )
        object.__setattr__(
            self,
            "indices_in_same_box",
            tuple(frozenset(index) for index in indices_in_same_box),
        )
        object.__setattr__(
            self, "collisions", tuple(frozenset(index) for index in collisions)
        )
