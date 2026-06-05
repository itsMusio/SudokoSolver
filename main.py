import tkinter as tk
from tkinter import ttk
import ctypes

from sudoku.application.solver import SudokuSolver
from sudoku.domain.board import InvalidBoardError, SudokuBoard
from sudoku.domain.validation import SudokuBoardValidator


CELL_BG = "#fffaf0"
CELL_USER_BG = "#dbeafe"
CELL_ERROR_BG = "#7f1d1d"
CELL_ERROR_FG = "#fee2e2"
CELL_TEXT = "#1f2933"
SOLVE_BG = "#2563eb"
SOLVE_HOVER_BG = "#1d4ed8"
SOLVE_PRESSED_BG = "#1e40af"
SOLVE_DISABLED_BG = "#334155"
SOLVE_DISABLED_FG = "#94a3b8"


class SudokuSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.title("Sudoku Solver")
        self.resizable(False, False)

        self.cells = []
        self.solver = SudokuSolver()
        self.validator = SudokuBoardValidator()
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._corner_radius = 18
        self.status_label = None
        self.solve_button = None
        self.solve_button_enabled = True
        self.cell_issues = {}
        self.tooltip = None

        self._configure_style()
        self._build_layout()
        self._validate_puzzle()
        self.after(10, self._apply_rounded_corners)

    def _configure_style(self):
        self.configure(bg="#111827")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Header.TLabel",
            background="#111827",
            foreground="#f9fafb",
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Subtle.TLabel",
            background="#111827",
            foreground="#cbd5e1",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#ffffff",
            background="#2563eb",
            padding=(18, 8),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
        )

    def _build_layout(self):
        root = tk.Frame(self, bg="#111827", padx=1, pady=1)
        root.grid(row=0, column=0)
        self._make_draggable(root)

        self._build_title_bar(root)

        container = tk.Frame(root, bg="#111827", padx=20, pady=18)
        container.grid(row=1, column=0)
        self._make_draggable(container)

        title = ttk.Label(container, text="Sudoku Solver", style="Header.TLabel")
        title.grid(row=0, column=0, sticky="w")
        self._make_draggable(title)

        subtitle = ttk.Label(
            container,
            text="Enter a puzzle here later. For now, this is our empty board.",
            style="Subtle.TLabel",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 14))
        self._make_draggable(subtitle)

        board = tk.Frame(container, bg="#111827")
        board.grid(row=2, column=0)

        for row in range(9):
            row_cells = []
            for col in range(9):
                cell_frame = tk.Frame(
                    board,
                    bg="#d1d5db",
                )
                cell_frame.grid(
                    row=row,
                    column=col,
                    padx=(3 if col % 3 == 0 else 1, 3 if col == 8 else 0),
                    pady=(3 if row % 3 == 0 else 1, 3 if row == 8 else 0),
                )

                cell = tk.Entry(
                    cell_frame,
                    width=2,
                    justify="center",
                    font=("Segoe UI", 18),
                    relief="flat",
                    bg=CELL_BG,
                    fg=CELL_TEXT,
                    insertbackground=CELL_TEXT,
                )
                cell.grid(
                    row=0,
                    column=0,
                    ipadx=6,
                    ipady=5,
                )
                cell.bind("<KeyRelease>", lambda _event: self._validate_puzzle())
                cell.bind("<Enter>", lambda event, r=row, c=col: self._show_cell_tooltip(event, r, c))
                cell.bind("<Leave>", lambda _event: self._hide_tooltip())
                row_cells.append(cell)
            self.cells.append(row_cells)

        actions = tk.Frame(container, bg="#111827")
        actions.grid(row=3, column=0, pady=(14, 0))
        self._make_draggable(actions)

        solve_button = tk.Label(
            actions,
            text="Solve",
            bg=SOLVE_BG,
            fg="#ffffff",
            font=("Segoe UI", 12, "bold"),
            padx=34,
            pady=10,
            cursor="hand2",
        )
        solve_button.grid(row=0, column=0, padx=(0, 10))
        self.solve_button = solve_button
        self._bind_title_button(
            solve_button,
            command=self._launch_solver,
            hover_bg=SOLVE_HOVER_BG,
            pressed_bg=SOLVE_PRESSED_BG,
        )

        flush_button = tk.Label(
            actions,
            text="Flush",
            bg="#374151",
            fg="#f9fafb",
            font=("Segoe UI", 12, "bold"),
            padx=32,
            pady=10,
            cursor="hand2",
        )
        flush_button.grid(row=0, column=1)
        self._bind_title_button(
            flush_button,
            command=self._flush_puzzle,
            hover_bg="#4b5563",
            pressed_bg="#6b7280",
        )

        self.status_label = ttk.Label(
            container,
            text="",
            style="Subtle.TLabel",
        )
        self.status_label.grid(row=4, column=0, pady=(10, 0))

    def _build_title_bar(self, parent):
        title_bar = tk.Frame(parent, bg="#111827", height=34)
        title_bar.grid(row=0, column=0, sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            title_bar,
            text="Sudoku Solver",
            bg="#111827",
            fg="#f9fafb",
            font=("Segoe UI", 10, "bold"),
            padx=12,
        )
        title.grid(row=0, column=0, sticky="w")

        minimize_button = tk.Label(
            title_bar,
            text="_",
            width=4,
            bg="#111827",
            fg="#f9fafb",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        minimize_button.grid(row=0, column=1, sticky="ns")

        close_button = tk.Label(
            title_bar,
            text="X",
            width=4,
            bg="#111827",
            fg="#f9fafb",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        close_button.grid(row=0, column=2, sticky="ns")

        self._bind_title_button(
            minimize_button,
            command=self._minimize_window,
            hover_bg="#1f2937",
            pressed_bg="#374151",
        )
        self._bind_title_button(
            close_button,
            command=self.destroy,
            hover_bg="#1f2937",
            pressed_bg="#374151",
        )

        for widget in (title_bar, title):
            self._make_draggable(widget)

    def _make_draggable(self, widget):
        widget.bind("<ButtonPress-1>", self._start_window_drag)
        widget.bind("<B1-Motion>", self._drag_window)

    def _bind_title_button(self, widget, command, hover_bg, pressed_bg):
        normal_bg = widget.cget("bg")

        widget.bind("<Enter>", lambda _event: self._hover_button(widget, hover_bg))
        widget.bind("<Leave>", lambda _event: self._leave_button(widget, normal_bg))
        widget.bind("<ButtonPress-1>", lambda _event: self._press_button(widget, pressed_bg))
        widget.bind(
            "<ButtonRelease-1>",
            lambda _event: self._activate_title_button(widget, command, hover_bg),
        )

    def _hover_button(self, widget, hover_bg):
        if widget == self.solve_button and not self.solve_button_enabled:
            return

        widget.configure(bg=hover_bg)

    def _leave_button(self, widget, normal_bg):
        if widget == self.solve_button and not self.solve_button_enabled:
            widget.configure(bg=SOLVE_DISABLED_BG)
            return

        widget.configure(bg=normal_bg)

    def _press_button(self, widget, pressed_bg):
        if widget == self.solve_button and not self.solve_button_enabled:
            return

        widget.configure(bg=pressed_bg)

    def _activate_title_button(self, widget, command, hover_bg):
        if widget == self.solve_button and not self.solve_button_enabled:
            return

        widget.configure(bg=hover_bg)
        command()

    def _start_window_drag(self, event):
        self._drag_start_x = event.x_root - self.winfo_x()
        self._drag_start_y = event.y_root - self.winfo_y()

    def _drag_window(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def _minimize_window(self):
        self.overrideredirect(False)
        self.iconify()
        self.bind("<Map>", self._restore_custom_title_bar)

    def _restore_custom_title_bar(self, _event):
        self.overrideredirect(True)
        self.unbind("<Map>")
        self.after(10, self._apply_rounded_corners)

    def _apply_rounded_corners(self):
        self.update_idletasks()

        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        width = self.winfo_width()
        height = self.winfo_height()
        diameter = self._corner_radius * 2

        region = ctypes.windll.gdi32.CreateRoundRectRgn(
            0,
            0,
            width + 1,
            height + 1,
            diameter,
            diameter,
        )
        ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    def _launch_solver(self):
        if not self.solve_button_enabled:
            self._set_status("Fix the highlighted cells before solving.", "#fca5a5")
            return

        try:
            board = self._read_board_from_cells()
            solved_board = self.solver.solve(board)
        except InvalidBoardError as error:
            self._set_status(str(error), "#fca5a5")
            return

        self._write_board_to_cells(solved_board)
        self._set_status("Puzzle solved.", "#86efac")
        self._validate_puzzle()

    def _flush_puzzle(self):
        for row in self.cells:
            for cell in row:
                cell.delete(0, tk.END)

        self._set_status("Puzzle cleared.", "#cbd5e1")
        self._validate_puzzle()

    def _read_board_from_cells(self):
        rows = []
        for row in self.cells:
            values = []
            for cell in row:
                text = cell.get().strip()
                if text == "":
                    values.append(0)
                    continue

                if not text.isdigit() or int(text) not in range(1, 10):
                    raise InvalidBoardError("Cells must be empty or contain a digit from 1 to 9.")

                values.append(int(text))
            rows.append(values)

        return SudokuBoard.from_rows(rows)

    def _write_board_to_cells(self, board):
        for row_index, row in enumerate(board.grid):
            for col_index, value in enumerate(row):
                cell = self.cells[row_index][col_index]
                cell.delete(0, tk.END)
                cell.insert(0, str(value))

    def _set_status(self, message, color):
        self.status_label.configure(text=message, foreground=color)

    def _validate_puzzle(self):
        rows, issues = self._read_rows_for_validation()

        try:
            board = SudokuBoard.from_rows(rows)
            for issue in self.validator.find_issues(board):
                self._add_cell_issue(issues, issue.row, issue.col, issue.message)
        except InvalidBoardError as error:
            self._set_status(str(error), "#fca5a5")

        self.cell_issues = issues
        self._paint_cells()

        if issues:
            self._set_solve_enabled(False)
            self._set_status(self._summarize_issues(issues), "#fca5a5")
        else:
            self._set_solve_enabled(True)
            if self.status_label.cget("text").startswith("Fix "):
                self._set_status("", "#cbd5e1")

    def _read_rows_for_validation(self):
        rows = []
        issues = {}

        for row_index, row in enumerate(self.cells):
            values = []
            for col_index, cell in enumerate(row):
                text = cell.get().strip()
                if text == "":
                    values.append(0)
                    continue

                if not text.isdigit():
                    values.append(0)
                    self._add_cell_issue(
                        issues,
                        row_index,
                        col_index,
                        "Only digits from 1 to 9 are allowed.",
                    )
                    continue

                value = int(text)
                if value not in range(1, 10):
                    values.append(0)
                    self._add_cell_issue(
                        issues,
                        row_index,
                        col_index,
                        "Use a digit from 1 to 9. Zero is treated as invalid input.",
                    )
                    continue

                values.append(value)
            rows.append(values)

        return rows, issues

    def _add_cell_issue(self, issues, row, col, message):
        issues.setdefault((row, col), [])
        if message not in issues[(row, col)]:
            issues[(row, col)].append(message)

    def _paint_cells(self):
        for row_index, row in enumerate(self.cells):
            for col_index, cell in enumerate(row):
                if (row_index, col_index) in self.cell_issues:
                    cell.configure(
                        bg=CELL_ERROR_BG,
                        fg=CELL_ERROR_FG,
                        insertbackground=CELL_ERROR_FG,
                    )
                else:
                    text = cell.get().strip()
                    bg_color = CELL_USER_BG if text else CELL_BG
                    cell.configure(
                        bg=bg_color,
                        fg=CELL_TEXT,
                        insertbackground=CELL_TEXT,
                    )

    def _set_solve_enabled(self, enabled):
        self.solve_button_enabled = enabled
        if enabled:
            self.solve_button.configure(bg=SOLVE_BG, fg="#ffffff", cursor="hand2")
        else:
            self.solve_button.configure(
                bg=SOLVE_DISABLED_BG,
                fg=SOLVE_DISABLED_FG,
                cursor="arrow",
            )

    def _summarize_issues(self, issues):
        total = len(issues)
        if total == 1:
            return "Fix 1 highlighted cell before solving."

        return f"Fix {total} highlighted cells before solving."

    def _show_cell_tooltip(self, event, row, col):
        messages = self.cell_issues.get((row, col))
        if not messages:
            return

        self._hide_tooltip()

        self.tooltip = tk.Toplevel(self)
        self.tooltip.overrideredirect(True)
        self.tooltip.configure(bg="#fca5a5")

        label = tk.Label(
            self.tooltip,
            text="\n".join(messages),
            bg="#7f1d1d",
            fg="#fee2e2",
            font=("Segoe UI", 9),
            justify="left",
            padx=10,
            pady=7,
        )
        label.grid(row=0, column=0, padx=1, pady=1)

        self.tooltip.geometry(f"+{event.x_root + 12}+{event.y_root + 14}")

    def _hide_tooltip(self):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None


def main():
    app = SudokuSolverApp()
    app.mainloop()


if __name__ == "__main__":
    main()
