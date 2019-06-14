from itertools import chain, combinations

from sudoku_solver.lib.constants import SudokuConstants


class SudokuPuzzle:
    __slots__ = ("candidates", "cells", "constants")
    top = "┌─────┬─────┬─────┐"
    mid = "├─────┼─────┼─────┤"
    bottom = "└─────┴─────┴─────┘"

    def __init__(self, string: str) -> None:
        self.constants = SudokuConstants()
        self.cells = list(string)
        self.candidates = self._get_candidates()

    def __str__(self) -> str:
        return "".join(self.cells)

    def __repr__(self) -> str:
        return f"SudokuPuzzle({self})"

    def format(self, *, pretty: bool) -> str:
        return self.matrix if pretty else str(self)

    def solve(self) -> bool:
        while "." in self.cells:
            if not self._advance():
                return False
        return True

    @property
    def matrix(self) -> str:
        rows = [
            self.top,
            self._format_row(0),
            self._format_row(1),
            self._format_row(2),
            self.mid,
            self._format_row(3),
            self._format_row(4),
            self._format_row(5),
            self.mid,
            self._format_row(6),
            self._format_row(7),
            self._format_row(8),
            self.bottom,
        ]
        return "\n".join(rows) + "\n"

    @property
    def debug_info(self) -> str:
        output = f"cells: {self}\ncandidates: {{\n"
        for i in range(81):
            if self.cells[i] == ".":
                output += f"\t{self._format_cell_id(i)}({i:02}):"
                if not self.candidates.get(i, []):
                    output += " no candidates,\n"
                else:
                    output += " {"
                    for candidate in sorted(self.candidates[i]):
                        output += f"{candidate}, "
                    output += "\b\b},\n"
        output += "}\n"
        return output

    def _get_candidates(self) -> dict[int, set[str]]:
        candidates = {}
        for i in range(81):
            if self.cells[i] == ".":
                temp_digits = set(self.constants.digits)
                for j in self.constants.collisions[i]:
                    temp_digits.discard(self.cells[j])
                candidates[i] = temp_digits
        return candidates

    @staticmethod
    def _format_cell_id(cell_index: int) -> str:
        row_id = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        return f"{row_id[cell_index // 9]}{(cell_index % 9) + 1}"

    def _format_row(self, row: int) -> str:
        start = 9 * row
        return (
            f"│{self.cells[start]} {self.cells[start + 1]} {self.cells[start + 2]}│"
            f"{self.cells[start + 3]} {self.cells[start + 4]} {self.cells[start + 5]}│"
            f"{self.cells[start + 6]} {self.cells[start + 7]} {self.cells[start + 8]}│"
        )

    def _advance(self) -> bool:
        return self._advance_cells() or self._advance_candidates()

    def _advance_cells(self) -> bool:
        return self._naked_single() or self._hidden_single()

    def _advance_candidates(self) -> bool:
        return (
            self._naked_pair()
            or self._hidden_pair()
            or self._locked_candidates()
            or self._x_wing()
        )

    def set_and_clean(self, index: int, digit: str) -> None:
        self.cells[index] = digit
        del self.candidates[index]
        for i in self.constants.collisions[index]:
            self.candidates.get(i, set()).discard(digit)

    def _naked_single(self) -> bool:
        """Advance using the naked single method.

        If a cell has only one candidate, set it and remove it from the candidates.
        """
        advanced = False
        for index in set(self.candidates.keys()):
            if len(self.candidates[index]) == 1:
                self.set_and_clean(index, self.candidates[index].pop())
                advanced = True
        return advanced

    def _hidden_single(self) -> bool:
        """Advance using the hidden single method.

        If a digit only appears once in the candidates of a row, column, or box,
        set it and remove it from the candidates.
        """
        advanced = False
        for index in set(self.candidates.keys()):
            blocks = [
                self.constants.indices_in_same_row[index],
                self.constants.indices_in_same_column[index],
                self.constants.indices_in_same_box[index],
            ]
            for block in blocks:
                unique = self.candidates[index].copy()
                for i in block:
                    for digit in self.candidates.get(i, set()):
                        unique.discard(digit)
                if len(unique) == 1:
                    self.set_and_clean(index, unique.pop())
                    advanced = True
                    break
        return advanced

    def _naked_pair_for_group(self, group: frozenset[int]) -> bool:
        advanced = False
        indices = group & set(self.candidates.keys())
        if len(indices) <= 2:  # noqa: PLR2004
            return advanced

        for index_1, index_2 in combinations(indices, 2):
            digits = self.candidates[index_1]
            if len(digits) != 2 or digits != self.candidates[index_2]:  # noqa: PLR2004
                continue
            for index in indices - {index_1, index_2}:
                for digit in digits:
                    if digit in self.candidates[index]:
                        self.candidates[index].discard(digit)
                        advanced = True
        return advanced

    def _naked_pair(self) -> bool:
        """Advance using the naked pair method.

        If two cells in a group have the same two candidates,
        remove those candidates from the other cells in the group.
        """
        advanced = False
        for group in chain(
            self.constants.rows, self.constants.columns, self.constants.boxes
        ):
            advanced |= self._naked_pair_for_group(group)
        return advanced

    def _hidden_pair_for_group(self, group: frozenset[int]) -> bool:
        advanced = False
        indices = group & set(self.candidates.keys())
        if len(indices) <= 2:  # noqa: PLR2004
            return advanced

        for index_1, index_2 in combinations(indices, 2):
            if (
                len(self.candidates[index_1] | self.candidates[index_2]) == 2  # noqa: PLR2004
            ):
                continue
            common = self.candidates[index_1] & self.candidates[index_2]
            other = set()
            for index in indices - {index_1, index_2}:
                other |= self.candidates[index]
            hidden = common - other
            if len(hidden) != 2:  # noqa: PLR2004
                continue
            self.candidates[index_1] = hidden.copy()
            self.candidates[index_2] = hidden.copy()
            advanced = True
        return advanced

    def _hidden_pair(self) -> bool:
        """Advance using the hidden pair method.

        If two digits only appear in two cells in a group,
        remove all other candidates from those cells.
        """
        advanced = False
        for group in chain(
            self.constants.rows, self.constants.columns, self.constants.boxes
        ):
            advanced |= self._hidden_pair_for_group(group)
        return advanced

    def _locked_candidates_for_groups(
        self, box: frozenset[int], line: frozenset[int]
    ) -> bool:
        advanced = False
        unfilled = set(self.candidates.keys())
        common = box & line & unfilled
        if not common:
            return advanced

        outside_line = (line - box) & unfilled
        outside_box = (box - line) & unfilled
        if not outside_line or not outside_box:
            return advanced

        common_digits = {digit for index in common for digit in self.candidates[index]}
        outside_line_digits = {
            digit for index in outside_line for digit in self.candidates[index]
        }
        outside_box_digits = {
            digit for index in outside_box for digit in self.candidates[index]
        }
        line_only_digits = common_digits - outside_line_digits
        if line_only_digits & outside_box_digits:
            advanced = True
            for index in outside_box:
                self.candidates[index] -= line_only_digits

        box_only_digits = common_digits - outside_box_digits
        if box_only_digits & outside_line_digits:
            advanced = True
            for index in outside_line:
                self.candidates[index] -= box_only_digits
        return advanced

    def _locked_candidates(self) -> bool:
        """Advance using the locked candidates method.

        If a digit only appears in a box in a row or column, or in a row,
        or column in a box, remove it from the rest of the row or column.
        """
        advanced = False
        for box in self.constants.boxes:
            for line in chain(self.constants.rows, self.constants.columns):
                advanced |= self._locked_candidates_for_groups(box, line)
        return advanced

    def _x_wing_for_cells(self, a: int, b: int) -> bool:
        first_row = set(self.constants.indices_in_same_row[a])
        if b in first_row:
            return False
        second_row = set(self.constants.indices_in_same_row[b])
        first_column = set(self.constants.indices_in_same_column[a])
        if b in first_column:
            return False
        second_column = set(self.constants.indices_in_same_column[b])
        c = first_row.intersection(second_column).pop()
        if c not in self.candidates:
            return False
        d = second_row.intersection(first_column).pop()
        if d not in self.candidates:
            return False
        common_indices = {a, b, c, d}
        common_digits = set.intersection(
            *(self.candidates[index] for index in common_indices)
        )
        if not common_digits:
            return False
        row_indices = (
            first_row.union(second_row)
            .intersection(self.candidates)
            .difference(common_indices)
        )
        row_digits = {
            digit for index in row_indices for digit in self.candidates[index]
        }
        column_indices = (
            first_column.union(second_column)
            .intersection(self.candidates)
            .difference(common_indices)
        )
        column_digits = {
            digit for index in column_indices for digit in self.candidates[index]
        }
        for digit in common_digits:
            if digit not in row_digits and digit in column_digits:
                for index in column_indices:
                    self.candidates[index].discard(digit)
                return True
            if digit not in column_digits and digit in row_digits:
                for index in row_indices:
                    self.candidates[index].discard(digit)
                return True
        return False

    def _x_wing(self) -> bool:
        """Advance using the x-wing method.

        If a digit only appears in two cells in a row or column,
        and this digit only appears in the equivalent cells in another row or column,
        this digit can be removed from the rest of the row or column.
        """
        advanced = False
        for a, b in combinations(self.candidates, 2):
            advanced |= self._x_wing_for_cells(a, b)
        return advanced
