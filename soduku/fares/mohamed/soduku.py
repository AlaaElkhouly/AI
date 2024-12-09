import tkinter as tk
from tkinter import messagebox
import random
import time
class Sudoku:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):
        """Check if placing `num` at (row, col) is valid."""
        # Check row
        if num in self.board[row]:
            return False
        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve_backtracking(self):
        """Solve the Sudoku using Backtracking."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # Empty cell
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve_backtracking():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.sudoku = Sudoku()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        """Create the Sudoku board with entry widgets."""
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=9)

    def read_board(self):
        """Read the board from the GUI."""
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                if value.isdigit():
                    self.sudoku.board[row][col] = int(value)
                else:
                    self.sudoku.board[row][col] = 0

    def update_board(self):
        """Update the GUI with the solved board."""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.sudoku.board[row][col]))

    def solve(self):
        """Solve the Sudoku puzzle and update the GUI."""
        self.read_board()
        if self.sudoku.solve_backtracking():
            self.update_board()
            messagebox.showinfo("Success", "Sudoku solved!")
        else:
            messagebox.showerror("Error", "This Sudoku puzzle cannot be solved.")

from collections import defaultdict

class ArcConsistency:
    def __init__(self, board):
        self.board = board
        self.domains = defaultdict(lambda: list(range(1, 10)))

    def initialize_domains(self):
        """Initialize domains based on the initial Sudoku board."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.domains[(row, col)] = [self.board[row][col]]

    def revise(self, xi, xj):
        """Revise the domain of xi with respect to xj."""
        revised = False
        for value in self.domains[xi]:
            if not any(self.is_consistent(value, other) for other in self.domains[xj]):
                self.domains[xi].remove(value)
                revised = True
        return revised

    def is_consistent(self, value, other):
        """Check if two values are consistent (not equal)."""
        return value != other

    def enforce_arc_consistency(self):
        """Apply arc consistency to the Sudoku CSP."""
        arcs = [(xi, xj) for xi in self.domains for xj in self.domains if xi != xj]
        while arcs:
            xi, xj = arcs.pop(0)
            if self.revise(xi, xj):
                for xk in self.get_neighbors(xi):
                    arcs.append((xk, xi))

    def get_neighbors(self, cell):
        """Get all neighbors of a cell."""
        row, col = cell
        neighbors = []
        for i in range(9):
            if i != col:
                neighbors.append((row, i))
            if i != row:
                neighbors.append((i, col))
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != cell:
                    neighbors.append((i, j))
        return neighbors


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
