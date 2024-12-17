import tkinter as tk
from tkinter import messagebox
from dokusan import generators


class CSP:
    def __init__(self):
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {var: list(range(1, 10)) for var in self.variables}
        self.neighbors = {
            (i, j): set((i, jj) for jj in range(9)) |
                     set((ii, j) for ii in range(9)) |
                     set((ii, jj) for ii in range(i // 3 * 3, (i // 3 + 1) * 3)
                         for jj in range(j // 3 * 3, (j // 3 + 1) * 3)) - {(i, j)}
            for i in range(9) for j in range(9)
        }

    def is_consistent(self, variable, value, assignment):
        """Check if assigning `value` to `variable` is consistent."""
        for neighbor in self.neighbors[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def select_unassigned_variable(self, assignment):
        """Use Minimum Remaining Values (MRV) heuristic to select the next variable."""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, variable, assignment):
        """Order domain values using the least-constraining value heuristic."""
        return sorted(self.domains[variable], key=lambda value: sum(
            value in self.domains[neighbor] for neighbor in self.neighbors[variable]
        ))

    def inference(self, variable, value, assignment):
        """Apply AC-3 algorithm to enforce arc consistency."""
        inferences = {}
        queue = [(variable, neighbor) for neighbor in self.neighbors[variable]]
        while queue:
            (Xi, Xj) = queue.pop(0)
            if self.revise(Xi, Xj):
                if not self.domains[Xi]:
                    return None
                for Xk in self.neighbors[Xi] - {Xj}:
                    queue.append((Xk, Xi))
        return inferences

    def revise(self, Xi, Xj):
        """Revise the domain of Xi to ensure arc consistency."""
        revised = False
        for x in self.domains[Xi][:]:
            if not any(x != y for y in self.domains[Xj]):
                self.domains[Xi].remove(x)
                revised = True
        return revised

    def backtrack(self, assignment={}):
        """Perform backtracking search."""
        if len(assignment) == len(self.variables):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                del assignment[variable] # Backtrack
        return None


# GUI for Sudoku Solver
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = {}
        self.original_values = {}
        self.sudoku_csp = CSP()

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

        generate_button = tk.Button(root, text="Generate Sudoku", command=self.generate_sudoku)
        generate_button.pack(pady=10)

        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.pack(pady=10)

    def draw_grid(self):
        """Draw grid lines on the Sudoku board."""
        for i in range(10):
            line_thickness = 3 if i % 3 == 0 else 1
            color = "black"
            self.canvas.create_line(50 * i, 0, 50 * i, 450, width=line_thickness, fill=color)
            self.canvas.create_line(0, 50 * i, 450, 50 * i, width=line_thickness, fill=color)

    def generate_sudoku(self):
        """Generate a Sudoku puzzle using the dokusan library."""
        self.clear_grid()
        puzzle = str(generators.random_sudoku(avg_rank=2000))  # Adjust avg_rank for difficulty
        self.sudoku_csp.domains = {var: list(range(1, 10)) for var in self.sudoku_csp.variables}
        for i in range(9):
            for j in range(9):
                value = int(puzzle[i * 9 + j])  # Extract the value from the flat string
                if value != 0:
                    self.cells[(i, j)].insert(0, str(value))
                    self.original_values[(i, j)] = value
                    self.sudoku_csp.domains[(i, j)] = [value]

    def clear_grid(self):
        """Clear the Sudoku grid."""
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
        self.original_values.clear()

    def solve(self):
        """Solve the Sudoku puzzle."""
        assignment = {}
        for i in range(9):
            for j in range(9):
                try:
                    value = int(self.cells[(i, j)].get())
                    if value in range(1, 10):
                        assignment[(i, j)] = value
                        self.sudoku_csp.domains[(i, j)] = [value]
                        self.original_values[(i, j)] = value
                except ValueError:
                    pass

        solution = self.sudoku_csp.backtrack(assignment)

        if solution:
            for i in range(9):
                for j in range(9):
                    self.cells[(i, j)].delete(0, tk.END)
                    self.cells[(i, j)].insert(0, solution[(i, j)])
                    if (i, j) not in self.original_values:
                        self.cells[(i, j)].config(fg="blue")
        else:
            messagebox.showerror("Error", "No solution found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
