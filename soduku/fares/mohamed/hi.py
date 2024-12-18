import queue
import tkinter as tk
from tkinter import messagebox, ttk, Frame
from dokusan import generators

# Variable Class
class Variable:
    def __init__(self, domain=None, value=0):
        self.value = value
        self.domain = domain if domain is not None else [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __str__(self):
        return str(self.value)

# State Class
class State:
    def __init__(self, grid):
        self.grid = grid
        self.variables = []
        for i in range(9):
            tmp = []
            for j in range(9):
                if grid[i][j] == 0:
                    tmp.append(Variable())
                else:
                    tmp.append(Variable(domain=[grid[i][j]], value=grid[i][j]))
            self.variables.append(tmp)

# Solver Functions
def is_valid_move(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def backtracking_solver(state, row=0, col=0):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if state.variables[row][col].value > 0:
        return backtracking_solver(state, row, col + 1)

    for num in range(1, 10):
        if is_valid_move(state.grid, row, col, num):
            state.grid[row][col] = num
            state.variables[row][col] = Variable(domain=[num], value=num)
            if backtracking_solver(state, row, col + 1):
                return True
            state.grid[row][col] = 0
            state.variables[row][col] = Variable()
    return False

# Enhanced GUI with Dotted Lines
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#f8f9fa")
        self.cell_size = 50  # Cell size in pixels
        self.create_widgets()

    def create_widgets(self):
        # Create a Canvas for the Sudoku grid
        self.canvas = tk.Canvas(self.root, width=9 * self.cell_size, height=9 * self.cell_size, bg="#ffffff")
        self.canvas.pack(padx=10, pady=10)
        self.draw_grid()

        # Place Entry widgets for cells
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                x0, y0 = j * self.cell_size, i * self.cell_size
                cell = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center', bg="#f9f9f9", fg="#333333",
                                bd=0, highlightthickness=0)
                cell.place(x=x0 + 12, y=y0 + 12, width=self.cell_size - 5, height=self.cell_size - 5)
                self.cells[i][j] = cell

        # Control Frame for buttons
        control_frame = Frame(self.root, bg="#f8f9fa")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Difficulty:", font=('Arial', 12), bg="#f8f9fa").grid(row=0, column=0, padx=5)
        self.difficulty_var = ttk.Combobox(control_frame, values=["Easy", "Medium", "Hard"], state="readonly", width=10)
        self.difficulty_var.current(0)
        self.difficulty_var.grid(row=0, column=1, padx=5)

        tk.Button(control_frame, text="Generate Puzzle", command=self.generate_puzzle, bg="#28a745", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Solve Puzzle", command=self.solve_sudoku, bg="#007bff", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=3, padx=5)

    def draw_grid(self):
        # Draw 3x3 grid bold lines
        for i in range(10):
            width = 3 if i % 3 == 0 else 1  # Bold lines for 3x3 grids
            dash = None if i % 3 == 0 else (3, 3)  # Dotted lines for internal cells
            self.canvas.create_line(0, i * self.cell_size, 9 * self.cell_size, i * self.cell_size, width=width, dash=dash)
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, 9 * self.cell_size, width=width, dash=dash)

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()
                row.append(int(value) if value.isdigit() else 0)
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(grid[i][j]))

    def generate_puzzle(self):
        difficulty = self.difficulty_var.get()
        avg_rank = {"Easy": 20, "Medium": 40, "Hard": 60}.get(difficulty, 20)
        puzzle = generators.random_sudoku(avg_rank=avg_rank)
        grid = [[int(str(puzzle)[i * 9 + j]) for j in range(9)] for i in range(9)]
        self.set_grid(grid)

    def solve_sudoku(self):
        grid = self.get_grid()
        state = State(grid)
        if backtracking_solver(state):
            self.set_grid(state.grid)
            messagebox.showinfo("Success", "Sudoku Solved Successfully!")
        else:
            messagebox.showerror("Error", "No solution exists for this Sudoku.")

# Main Program
if __name__ == '__main__':
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
