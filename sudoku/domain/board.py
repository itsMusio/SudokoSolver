from dataclasses import dataclass
from typing import Iterable


Grid = tuple[tuple[int, ...], ...]


class InvalidBoardError(ValueError):
    pass


@dataclass(frozen=True)
class SudokuBoard:
    grid: Grid

    @classmethod
    def from_rows(cls, rows: Iterable[Iterable[int]]) -> "SudokuBoard":
        grid = tuple(tuple(row) for row in rows)
        board = cls(grid)
        board._validate_shape_and_values()
        return board

    def _validate_shape_and_values(self):
        if len(self.grid) != 9:
            raise InvalidBoardError("Sudoku board must have exactly 9 rows.")

        for row in self.grid:
            if len(row) != 9:
                raise InvalidBoardError("Each Sudoku row must have exactly 9 values.")

            for value in row:
                if value < 0 or value > 9:
                    raise InvalidBoardError("Sudoku values must be between 0 and 9.")

    def with_value(self, row: int, col: int, value: int) -> "SudokuBoard":
        rows = [list(current_row) for current_row in self.grid]
        rows[row][col] = value
        return SudokuBoard.from_rows(rows)

    def is_empty_at(self, row: int, col: int) -> bool:
        return self.grid[row][col] == 0

    def has_empty_cells(self) -> bool:
        return any(0 in row for row in self.grid)

    def is_empty(self) -> bool:
        return all(value == 0 for row in self.grid for value in row)

    def values_in_row(self, row: int) -> set[int]:
        return set(self.grid[row]) - {0}

    def values_in_column(self, col: int) -> set[int]:
        return {self.grid[row][col] for row in range(9)} - {0}

    def values_in_box(self, row: int, col: int) -> set[int]:
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        values = set()
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                value = self.grid[current_row][current_col]
                if value != 0:
                    values.add(value)

        return values

    def candidates_for(self, row: int, col: int) -> set[int]:
        if not self.is_empty_at(row, col):
            return set()

        used_values = (
            self.values_in_row(row)
            | self.values_in_column(col)
            | self.values_in_box(row, col)
        )
        return set(range(1, 10)) - used_values

    def is_valid(self) -> bool:
        return (
            self._groups_are_valid(self.grid)
            and self._groups_are_valid(self._columns())
            and self._groups_are_valid(self._boxes())
        )

    def _columns(self) -> list[list[int]]:
        return [[self.grid[row][col] for row in range(9)] for col in range(9)]

    def _boxes(self) -> list[list[int]]:
        boxes = []
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                boxes.append(
                    [
                        self.grid[row][col]
                        for row in range(start_row, start_row + 3)
                        for col in range(start_col, start_col + 3)
                    ]
                )
        return boxes

    @staticmethod
    def _groups_are_valid(groups: Iterable[Iterable[int]]) -> bool:
        for group in groups:
            values = [value for value in group if value != 0]
            if len(values) != len(set(values)):
                return False

        return True
