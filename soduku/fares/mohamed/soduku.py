import tkinter as tk
from tkinter import ttk, messagebox

# AC-3 Algorithm
class State:
    def __init__(self, grid):
        self.grid = grid
        self.variables = self.initialize_variables()

    def initialize_variables(self):
        variables = {}
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    variables[(i, j)] = list(range(1, 10))  # All possible values
                else:
                    variables[(i, j)] = [self.grid[i][j]]  # Single value for filled cells
        return variables

    def get_neighbors(self, xi):
        neighbors = []
        i, j = xi
        for row in range(9):
            if row != i:
                neighbors.append((row, j))
        for col in range(9):
            if col != j:
                neighbors.append((i, col))
        # 3x3 block neighbors
        block_row, block_col = i // 3, j // 3
        for r in range(block_row * 3, (block_row + 1) * 3):
            for c in range(block_col * 3, (block_col + 1) * 3):
                if (r, c) != (i, j):
                    neighbors.append((r, c))
        return neighbors

    def ac3(self):
        queue = [(xi, xj) for xi in self.variables for xj in self.get_neighbors(xi)]
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.variables[xi]) == 0:
                    return False  # Failure
                for xk in self.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.variables[xi]:
            if not any(y != x for y in self.variables[xj]):
                self.variables[xi].remove(x)
                revised = True
        return revised

# Backtracking Solver with AC-3
def backtracking_solver_with_ac3(state):
    if all(len(domain) == 1 for domain in state.variables.values()):
        return True  # Solved
    var = select_unassigned_variable(state)
    for value in state.variables[var]:
        if is_consistent(state, var, value):
            state.grid[var[0]][var[1]] = value  # Assign value
            state.ac3()  # Apply AC-3 after assignment
            if backtracking_solver_with_ac3(state):
                return True
            state.grid[var[0]][var[1]] = 0  # Unassign
    return False

def select_unassigned_variable(state):
    unassigned = [(var, len(state.variables[var])) for var in state.variables if len(state.variables[var]) > 1]
    return min(unassigned, key=lambda x: x[1])[0]  # Select variable with the smallest domain

def is_consistent(state, var, value):
    # Check if assigning `value` to `var` doesn't violate constraints
    for neighbor in state.get_neighbors(var):
        if value in state.variables[neighbor]:
            return False
    return True

# GUI Class
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#f8f9fa")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        # Frame for the grid
        grid_frame = tk.Frame(self.root, bg="#333333", bd=5, relief="ridge")
        grid_frame.pack(padx=20, pady=20)

        # Create Sudoku grid with styled cells
        for i in range(9):
            for j in range(9):
                padx = (8, 16) if j % 3 == 2 else (4, 4)
                pady = (8, 16) if i % 3 == 2 else (4, 4)
                bg_color = "#fdfdfd" if (i // 3 + j // 3) % 2 == 0 else "#f0f0f0"
                cell = tk.Entry(grid_frame, width=3, font=('Arial', 20), justify='center', bd=1, relief='solid',
                                bg=bg_color, fg="#333333", highlightbackground="#aaa", highlightthickness=1)
                cell.grid(row=i, column=j, padx=padx, pady=pady)
                self.cells[i][j] = cell

        # Control Frame for buttons
        control_frame = tk.Frame(self.root, bg="#f8f9fa")
        control_frame.pack(pady=10)

        # Buttons
        tk.Button(control_frame, text="Generate Puzzle", command=self.generate_puzzle, bg="#28a745", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Solve Puzzle", command=self.solve_sudoku, bg="#007bff", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=1, padx=5)

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
        # Puzzle generation logic (for simplicity, we can use a fixed puzzle)
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.set_grid(puzzle)

    def solve_sudoku(self):
        grid = self.get_grid()
        state = State(grid)
        if backtracking_solver_with_ac3(state):
            self.set_grid(state.grid)
            messagebox.showinfo("Success", "Sudoku Solved Successfully!")
        else:
            messagebox.showerror("Error", "No solution exists for this Sudoku.")

# Main code to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
