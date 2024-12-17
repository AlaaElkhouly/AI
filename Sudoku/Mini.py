from collections import deque
import tkinter as tk
from tkinter import messagebox

# GUI Components
def toggle_mode():
    """Toggle between 'Mode 1' and 'Mode 2'."""
    if mode_button.config('text')[-1] == "Mode 1":
        mode_button.config(text="Mode 2")
    else:
        mode_button.config(text="Mode 1")

def restart():
    """Clear all cells in the Sudoku grid."""
    for i in range(9):
        for j in range(9):
            grid_entries[i][j].delete(0, tk.END)

def get_grid():
    """Retrieve the current grid as a 2D list."""
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            value = grid_entries[i][j].get()
            if value.isdigit():
                row.append(int(value))
            else:
                row.append(0)  # Empty cells are represented as 0
        grid.append(row)
    return grid

def display_grid(grid):
    """Display a 2D list in the GUI grid."""
    for i in range(9):
        for j in range(9):
            grid_entries[i][j].delete(0, tk.END)
            if grid[i][j] != 0:
                grid_entries[i][j].insert(0, str(grid[i][j]))

# Solver Functions
def is_valid(grid, row, col, num):
    """Check if placing a number in a cell is valid."""
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    # Check 3x3 subgrid
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False

    return True

def initialize_domains(grid):
    """Initialize domains for each cell."""
    domains = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:  # Pre-filled cell
                domains[i][j] = {grid[i][j]}
    return domains

def revise(domains, grid, xi, xj):
    """Revise domains to ensure arc consistency."""
    revised = False
    for x in domains[xi[0]][xi[1]].copy():
        if not any(is_valid(grid, xj[0], xj[1], x) for x in domains[xj[0]][xj[1]]):
            domains[xi[0]][xi[1]].remove(x)
            revised = True
    return revised

def ac3(domains, grid):
    """Apply the AC-3 algorithm."""
    queue = deque()
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:  # Only for unfilled cells
                neighbors = get_neighbors(i, j)
                for neighbor in neighbors:
                    queue.append(((i, j), neighbor))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, grid, xi, xj):
            if not domains[xi[0]][xi[1]]:
                return False  # No valid values, puzzle is unsolvable
            for neighbor in get_neighbors(xi[0], xi[1]):
                if neighbor != xj:
                    queue.append((neighbor, xi))
    return True

def get_neighbors(row, col):
    """Get all neighbors of a cell."""
    neighbors = set()
    for i in range(9):
        if i != row:
            neighbors.add((i, col))  # Same column
        if i != col:
            neighbors.add((row, i))  # Same row
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) != (row, col):
                neighbors.add((i, j))  # Same 3x3 subgrid
    return neighbors

def solve_sudoku_with_arc_consistency(grid):
    """Solve Sudoku with arc consistency and backtracking."""
    domains = initialize_domains(grid)
    if not ac3(domains, grid):
        return False  # Arc consistency failed

    return backtrack(grid, domains)

def backtrack(grid, domains):
    """Backtracking search with domains."""
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True  # Solved

    row, col = empty_cell
    for value in domains[row][col]:
        if is_valid(grid, row, col, value):
            grid[row][col] = value
            if backtrack(grid, domains):
                return True
            grid[row][col] = 0  # Backtrack
    return False

def find_empty_cell(grid):
    """Find the next empty cell."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve():
    """Solve the Sudoku puzzle and display the solution."""
    grid = get_grid()
    if solve_sudoku_with_arc_consistency(grid):
        display_grid(grid)
    else:
        messagebox.showerror("Error", "No solution exists for this puzzle.")

# GUI Setup
root = tk.Tk()
root.title("Sudoku GUI")
root.geometry("600x650")

grid_frame = tk.Frame(root, bg="white", bd=5)
grid_frame.pack(pady=5)

grid_entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        entry = tk.Entry(
            grid_frame,
            width=2,
            font=('Arial', 18),
            justify='center',
            relief="solid",
            bd=1
        )
        entry.grid(row=i, column=j, padx=2, pady=2)
        row_entries.append(entry)
    grid_entries.append(row_entries)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

mode_button = tk.Button(button_frame, text="Mode 1", command=toggle_mode, width=10, font=('Arial', 14))
mode_button.pack(side=tk.LEFT, padx=20)

restart_button = tk.Button(button_frame, text="Restart", command=restart, width=10, font=('Arial', 14))
restart_button.pack(side=tk.LEFT, padx=20)

solve_button = tk.Button(button_frame, text="Solve", command=solve, width=10, font=('Arial', 14))
solve_button.pack(side=tk.RIGHT, padx=20)

title_label = tk.Label(root, text="Sudoku Puzzle", font=('Arial', 20, 'bold'))
title_label.pack(pady=5)

root.mainloop()
