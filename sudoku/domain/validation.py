from dataclasses import dataclass
from typing import Iterable

from sudoku.domain.board import SudokuBoard


@dataclass(frozen=True)
class CellIssue:
    row: int
    col: int
    message: str


class SudokuBoardValidator:
    def find_issues(self, board: SudokuBoard) -> list[CellIssue]:
        issues = []

        issues.extend(self._find_duplicate_issues(self._row_groups(board)))
        issues.extend(self._find_duplicate_issues(self._column_groups(board)))
        issues.extend(self._find_duplicate_issues(self._box_groups(board)))

        return issues

    def _row_groups(self, board: SudokuBoard):
        for row in range(9):
            yield [
                (row, col, board.grid[row][col], f"Value is repeated in row {row + 1}.")
                for col in range(9)
            ]

    def _column_groups(self, board: SudokuBoard):
        for col in range(9):
            yield [
                (row, col, board.grid[row][col], f"Value is repeated in column {col + 1}.")
                for row in range(9)
            ]

    def _box_groups(self, board: SudokuBoard):
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                box_number = (start_row // 3) * 3 + (start_col // 3) + 1
                yield [
                    (
                        row,
                        col,
                        board.grid[row][col],
                        f"Value is repeated in 3x3 box {box_number}.",
                    )
                    for row in range(start_row, start_row + 3)
                    for col in range(start_col, start_col + 3)
                ]

    def _find_duplicate_issues(self, groups: Iterable[list[tuple[int, int, int, str]]]):
        issues = []

        for group in groups:
            positions_by_value = {}
            for row, col, value, message in group:
                if value == 0:
                    continue

                positions_by_value.setdefault(value, []).append((row, col, message))

            for positions in positions_by_value.values():
                if len(positions) < 2:
                    continue

                for row, col, message in positions:
                    issues.append(CellIssue(row, col, message))

        return issues
