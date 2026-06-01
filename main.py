import tkinter as tk
from tkinter import ttk
import ctypes


class SudokuSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.title("Sudoku Solver")
        self.resizable(False, False)

        self.cells = []
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._corner_radius = 18

        self._configure_style()
        self._build_layout()
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
                    bg="#fffaf0",
                    fg="#1f2933",
                    insertbackground="#1f2933",
                )
                cell.grid(
                    row=0,
                    column=0,
                    ipadx=6,
                    ipady=5,
                )
                row_cells.append(cell)
            self.cells.append(row_cells)

        solve_button = tk.Label(
            container,
            text="Solve",
            bg="#2563eb",
            fg="#ffffff",
            font=("Segoe UI", 12, "bold"),
            padx=34,
            pady=10,
            cursor="hand2",
        )
        solve_button.grid(row=3, column=0, pady=(14, 0))
        self._bind_title_button(
            solve_button,
            command=self._launch_solver,
            hover_bg="#1d4ed8",
            pressed_bg="#1e40af",
        )

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

        widget.bind("<Enter>", lambda _event: widget.configure(bg=hover_bg))
        widget.bind("<Leave>", lambda _event: widget.configure(bg=normal_bg))
        widget.bind("<ButtonPress-1>", lambda _event: widget.configure(bg=pressed_bg))
        widget.bind("<ButtonRelease-1>", lambda _event: self._activate_title_button(widget, command, hover_bg))

    def _activate_title_button(self, widget, command, hover_bg):
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
        print("Solver module will be connected here.")


def main():
    app = SudokuSolverApp()
    app.mainloop()


if __name__ == "__main__":
    main()
