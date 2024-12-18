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
        self.constraints = []
        for i in range(9):
            tmp = []
            for j in range(9):
                if grid[i][j] == 0:
                    tmp.append(Variable())
                else:
                    tmp.append(Variable(domain=[grid[i][j]], value=grid[i][j]))
            self.variables.append(tmp)
        self.createArcs()

    def createArcs(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if j != k:  # Row constraints
                        self.constraints.append((self.variables[i][j], self.variables[i][k]))
                    if i != k:  # Column constraints
                        self.constraints.append((self.variables[i][j], self.variables[k][j]))
                    if not (i == 3 * (i // 3) + (k // 3) and j == 3 * (j // 3) + k % 3):  # Block constraints
                        self.constraints.append((self.variables[i][j], self.variables[3 * (i // 3) + (k // 3)][3 * (j // 3) + k % 3]))

    def ac3(self, show_steps=False):
        queue = self.create_queue()
        step = 0
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(xi.domain) == 0:  # If domain is empty, no solution
                    return False
                for neighbor in self.get_neighbors(xi):
                    if neighbor != xj:
                        queue.append((neighbor, xi))
            if show_steps:
                step += 1
                self.show_domains(step)
        return True

    def create_queue(self):
        queue = []
        for xi, xj in self.constraints:
            queue.append((xi, xj))
        return queue

    def revise(self, xi, xj):
        revised = False
        for x in xi.domain[:]:  # Make a copy to iterate safely
            if not self.has_support(x, xi, xj):
                xi.domain.remove(x)
                revised = True
        return revised

    def has_support(self, x, xi, xj):
        for y in xj.domain:
            if x != y:
                return True
        return False

    def get_neighbors(self, var):
        neighbors = []
        for xi, xj in self.constraints:
            if xi == var:
                neighbors.append(xj)
            elif xj == var:
                neighbors.append(xi)
        return neighbors

    def show_domains(self, step):
        print(f"Step {step}: Domains after applying arc consistency:")
        for i in range(9):
            for j in range(9):
                print(f"({i}, {j}): {self.variables[i][j].domain}", end=" | ")
            print()
        print("-" * 50)

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                if len(self.variables[i][j].domain) == 1 and self.variables[i][j].value == 0:
                    self.variables[i][j].value = self.variables[i][j].domain[0]
                    self.grid[i][j] = self.variables[i][j].value

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
    if col == 9:  # Move to the next row
        if row == 8:
            return True
        row += 1
        col = 0

    if state.variables[row][col].value > 0:  # Skip pre-filled cells
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

# Enhanced GUI Class
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#f8f9fa")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        # Frame for the grid with spacing
        grid_frame = Frame(self.root, bg="#333333", bd=5, relief="ridge")
        grid_frame.pack(padx=20, pady=20)

        # Create Sudoku grid with styled cells and spacing for 3x3 grids
        for i in range(9):
            for j in range(9):
                # Padding for spacing between 3x3 grids
                padx = (8, 16) if j % 3 == 2 else (4, 4)  # Extra spacing on right side for every 3rd column
                pady = (8, 16) if i % 3 == 2 else (4, 4)  # Extra spacing below every 3rd row

                # Background color and styling
                bg_color = "#fdfdfd" if (i // 3 + j // 3) % 2 == 0 else "#f0f0f0"
                cell = tk.Entry(grid_frame, width=3, font=('Arial', 20), justify='center', bd=1, relief='solid',
                                bg=bg_color, fg="#333333", highlightbackground="#aaa", highlightthickness=1)
                cell.grid(row=i, column=j, padx=padx, pady=pady)
                self.cells[i][j] = cell

        # Control Frame for buttons and dropdown
        control_frame = Frame(self.root, bg="#f8f9fa")
        control_frame.pack(pady=10)

        # Difficulty selection
        tk.Label(control_frame, text="Difficulty:", font=('Arial', 12), bg="#f8f9fa").grid(row=0, column=0, padx=5)
        self.difficulty_var = ttk.Combobox(control_frame, values=["Easy", "Medium", "Hard"], state="readonly", width=10)
        self.difficulty_var.current(0)
        self.difficulty_var.grid(row=0, column=1, padx=5)

        # Buttons
        tk.Button(control_frame, text="Generate Puzzle", command=self.generate_puzzle, bg="#28a745", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Solve Puzzle", command=self.solve_sudoku, bg="#007bff", fg="white",
                  font=('Arial', 12), width=15).grid(row=0, column=3, padx=5)

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
        avg_rank = {"Easy": 10, "Medium": 100, "Hard": 1000000}.get(difficulty, 20)
        puzzle = generators.random_sudoku(avg_rank=avg_rank)
        grid = [[int(str(puzzle)[i * 9 + j]) for j in range(9)] for i in range(9)]
        self.set_grid(grid)

    def solve_sudoku(self):
        grid = self.get_grid()
        state = State(grid)
        if state.ac3(show_steps=True):  # Show Arc Consistency Steps
            state.update_grid()
            if backtracking_solver(state):
                self.set_grid(state.grid)
                messagebox.showinfo("Success", "Sudoku Solved Successfully!")
            else:
                messagebox.showerror("Error", "No solution exists.")
        else:
            messagebox.showerror("Error", "No solution exists.")

# Main Application
def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
