# Sudoku Solver

A small desktop Sudoku solver built with Python and Tkinter. The app provides a 9x9 board for entering puzzles, validates duplicate values as you type, and solves puzzles with a backtracking solver that rejects empty, invalid, unsolvable, or non-unique boards.

## Features

- Tkinter desktop interface with a custom title bar
- Live validation for duplicate values in rows, columns, and 3x3 boxes
- Backtracking Sudoku solver with candidate pruning
- Detection for puzzles with no solution or more than one solution
- Clear/flush action for resetting the board
- Unit tests for solver and validation behavior
- PyInstaller publishing script for building a Windows executable

## Requirements

- Python 3.10 or newer recommended
- Windows for the included `.bat` helper scripts
- No third-party runtime packages are currently required

Tkinter is included with the standard Python installer on Windows.

## Quick Start

On Windows, run:

```bat
run.bat
```

The script creates a local virtual environment if needed, checks `requirements.txt`, and starts the application.

## Manual Setup

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Running Tests

```powershell
python -m unittest
```

## Building an Executable

Use the included publishing script:

```bat
publish.bat
```

This installs the build requirements and creates:

```text
dist\SudokuSolver.exe
```

You can also run PyInstaller manually:

```powershell
python -m pip install -r build-requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name SudokuSolver main.py
```

## Project Structure

```text
.
|-- main.py                         # Tkinter application entry point
|-- sudoku/
|   |-- application/
|   |   `-- solver.py               # Sudoku solving logic
|   `-- domain/
|       |-- board.py                # Immutable board model and board rules
|       `-- validation.py           # Duplicate-cell validation
|-- tests/
|   `-- test_solver.py              # Unit tests
|-- run.bat                         # Windows run helper
|-- publish.bat                     # Windows build helper
|-- requirements.txt                # Runtime dependencies
`-- build-requirements.txt          # Build dependencies
```

## Solver Usage

The solver can also be used directly from Python:

```python
from sudoku.application.solver import SudokuSolver
from sudoku.domain.board import SudokuBoard

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

solution = SudokuSolver().solve(puzzle)

for row in solution.grid:
    print(row)
```

Use `0` for empty cells.

## Notes

- The solver requires a valid puzzle with exactly one solution.
- Invalid board shapes or values outside `0` through `9` raise `InvalidBoardError`.
- Empty cells are represented by `0`.
