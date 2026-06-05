import unittest

from sudoku.application.solver import SudokuSolver
from sudoku.domain.board import InvalidBoardError, SudokuBoard
from sudoku.domain.validation import SudokuBoardValidator


class SudokuSolverTests(unittest.TestCase):
    def test_solves_valid_puzzle(self):
        puzzle = SudokuBoard.from_rows(
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )

        solved = SudokuSolver().solve(puzzle)

        self.assertEqual(solved.grid[0], (5, 3, 4, 6, 7, 8, 9, 1, 2))
        self.assertFalse(solved.has_empty_cells())
        self.assertTrue(solved.is_valid())

    def test_rejects_invalid_puzzle(self):
        puzzle = SudokuBoard.from_rows(
            [
                [5, 5, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )

        with self.assertRaises(InvalidBoardError):
            SudokuSolver().solve(puzzle)

    def test_rejects_empty_puzzle(self):
        puzzle = SudokuBoard.from_rows([[0] * 9 for _ in range(9)])

        with self.assertRaisesRegex(InvalidBoardError, "empty board"):
            SudokuSolver().solve(puzzle)

    def test_rejects_puzzle_with_multiple_solutions(self):
        puzzle = SudokuBoard.from_rows(
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        with self.assertRaisesRegex(InvalidBoardError, "more than one solution"):
            SudokuSolver().solve(puzzle)


class SudokuBoardValidatorTests(unittest.TestCase):
    def test_reports_duplicate_cells_by_group(self):
        board = SudokuBoard.from_rows(
            [
                [5, 5, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )

        issues = SudokuBoardValidator().find_issues(board)
        issue_cells = {(issue.row, issue.col) for issue in issues}

        self.assertIn((0, 0), issue_cells)
        self.assertIn((0, 1), issue_cells)


if __name__ == "__main__":
    unittest.main()
