from sudoku.domain.board import InvalidBoardError, SudokuBoard


class SudokuSolver:
    def solve(self, board: SudokuBoard) -> SudokuBoard:
        if board.is_empty():
            raise InvalidBoardError("Enter a puzzle before solving. An empty board is not useful.")

        if not board.is_valid():
            raise InvalidBoardError("This puzzle has repeated values in a row, column, or box.")

        solutions = self._find_solutions(board, limit=2)
        if not solutions:
            raise InvalidBoardError("This puzzle has no valid solution.")

        if len(solutions) > 1:
            raise InvalidBoardError("This puzzle has more than one solution. Add more clues before solving.")

        return solutions[0]

    def _find_solutions(self, board: SudokuBoard, limit: int) -> list[SudokuBoard]:
        empty_cell = self._find_best_empty_cell(board)
        if empty_cell is None:
            return [board]

        row, col, candidates = empty_cell
        if not candidates:
            return []

        solutions = []

        for value in sorted(candidates):
            solutions.extend(self._find_solutions(board.with_value(row, col, value), limit))
            if len(solutions) >= limit:
                return solutions

        return solutions

    def _find_best_empty_cell(self, board: SudokuBoard) -> tuple[int, int, set[int]] | None:
        best_cell = None

        for row in range(9):
            for col in range(9):
                if not board.is_empty_at(row, col):
                    continue

                candidates = board.candidates_for(row, col)
                if best_cell is None or len(candidates) < len(best_cell[2]):
                    best_cell = (row, col, candidates)

                if len(candidates) == 1:
                    return best_cell

        return best_cell
