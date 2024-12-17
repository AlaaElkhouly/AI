import tkinter as tk
from tkinter import messagebox
#____________________Solves Puzzles the user enters_________________#
variables = [(i, j) for i in range(9) for j in range(9)]              #List of all the cells
domains = {var: list(range(1, 10)) for var in variables}              # possible values that a variable can take
neighbors = {(i, j): set((i, jj) for jj in range(9)) |  # same row
                     set((ii, j) for ii in range(9)) |  # same column                        
                     set((ii, jj) for ii in range(i // 3 * 3, (i // 3 + 1) * 3) for jj in
                         range(j // 3 * 3, (j // 3 + 1) * 3)) - {(i, j)}       # same 3x3 subgrid
             for i in range(9) for j in range(9)}

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

    # Check if the value assignment is consistent by satisfying all constraints
    def is_consistent(self, var, value, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and not self.constraints(var, value, neighbor, assignment[neighbor]):
                return False
        return True


def select_unassigned_variable(assignment, csp):
    # Selects the next variable (cell) that has not yet been assigned a value
    # Iterates through all variables and returns the first unassigned one
    return next(var for var in csp.variables if var not in assignment)


def order_domain_values(var, assignment, csp):
    # Returns the list of possible values for a variable
    return csp.domains[var]


def backtrack(assignment, csp):
    # Recursive backtracking algorithm

    # Checks if all variables are assigned
    if len(assignment) == len(csp.variables):
        return assignment

    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            inferences = inference(csp, assignment, var, value)
            if inferences is not None:
                result = backtrack(assignment, csp)
                if result is not None:
                    return result
            del assignment[var]
    return None


# Arc Consistency
def inference(csp, assignment, var, value):
    # Apply inference to reduce the domains of other variables
    queue = [(var, neighbor) for neighbor in csp.neighbors[var]]
    while queue:
        (Xi, Xj) = queue.pop(0)
        if revise(csp, Xi, Xj):
            if not csp.domains[Xi]:
                return None
            for Xk in csp.neighbors[Xi] - {Xj}:
                queue.append((Xk, Xi))
    return assignment


def revise(csp, Xi, Xj):
    # Revise the domain of Xi to ensure consistency with Xj
    revised = False
    for x in csp.domains[Xi][:]:
        if not any(csp.constraints(Xi, x, Xj, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
    return revised


def sudoku_constraints(A, a, B, b):
    # ensure no two variables in the same row, column, or box have the same value
    return a != b
##################################################################

# GUI for Sudoku
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = {}
        self.original_values = {}

        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=450, height=450)
        self.canvas.pack()

        for i in range(9):
            for j in range(9):
                x0 = j * 50
                y0 = i * 50
                x1 = x0 + 50
                y1 = y0 + 50

                entry = tk.Entry(frame, width=3, font=("Arial", 18), justify="center", bd=1, relief="solid")
                entry.place(x=x0 + 5, y=y0 + 5, width=40, height=40)
                self.cells[(i, j)] = entry

        self.draw_grid()

        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.pack(pady=10)

    def draw_grid(self):
        for i in range(10):
            line_thickness = 3 if i % 3 == 0 else 1
            color = "black"
            self.canvas.create_line(50 * i, 0, 50 * i, 450, width=line_thickness, fill=color)
            self.canvas.create_line(0, 50 * i, 450, 50 * i, width=line_thickness, fill=color)

    def solve(self):
        assignment = {}
        for i in range(9):
            for j in range(9):
                try:
                    value = int(self.cells[(i, j)].get())
                    if value in range(1, 10):
                        assignment[(i, j)] = value
                        domains[(i, j)] = [value]
                        self.original_values[(i, j)] = value
                except ValueError:
                    pass

        print("Initial assignment:", assignment)

        sudoku_csp = CSP(variables, domains, neighbors, sudoku_constraints)

        solution = backtrack(assignment, sudoku_csp)

        if solution:
            for i in range(9):
                for j in range(9):
                    self.cells[(i, j)].delete(0, tk.END)
                    self.cells[(i, j)].insert(0, solution[(i, j)])
                    if (i, j) not in self.original_values:
                        self.cells[(i, j)].config(fg="blue")
        else:
            messagebox.showerror("Error", "No solution found.")
            print("No solution found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
