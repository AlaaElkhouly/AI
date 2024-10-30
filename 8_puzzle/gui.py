import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import Astar
class PuzzleSolverGUI:
    def __init__(self, root):
        self.root = root #root window
        self.root.title("8-Puzzle Solver")
        self.board_size = 3
        self.board = [[None] * self.board_size for _ in range(self.board_size)] #create 3*3 board elly later 77ot feeha el 7aga
        self.start_state = []
        self.solution_states = []  # Will be populated after solving
        self.init_ui()

    def init_ui(self):
        # Create grid for puzzle board
        self.create_board_grid()
        
        # Algorithm selection
        self.algorithm_var = tk.StringVar(value="A*")
        algo_frame = tk.Frame(self.root) #algorithm slelection window
        algo_frame.pack()# add to root window
        tk.Label(algo_frame, text="Select Algorithm: ").pack(side=tk.LEFT) #prompt user to choose alogrithm
        tk.OptionMenu(algo_frame, self.algorithm_var, "BFS", "DFS", "IDFS", "A*").pack(side=tk.LEFT)

        # Heuristic selection for A*
        self.heuristic_var = tk.StringVar(value="Manhattan")
        tk.Label(algo_frame, text="Heuristic: ").pack(side=tk.LEFT)
        tk.OptionMenu(algo_frame, self.heuristic_var, 1, 0).pack(side=tk.LEFT)
        
        # Buttons to enter state, solve, and show solution
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        tk.Button(control_frame, text="Enter Start State", command=self.enter_start_state).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Solve", command=self.solve_puzzle).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Animate Solution", command=self.animate_solution).pack(side=tk.LEFT)

    def create_board_grid(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack()
        for i in range(self.board_size):
            for j in range(self.board_size):
                label = tk.Label(board_frame, text="", font=("Arial", 24), width=4, height=2, borderwidth=2, relief="solid")
                label.grid(row=i, column=j)
                self.board[i][j] = label

    def enter_start_state(self):
        # Prompt user to enter a 9-tile puzzle start state
        state = simpledialog.askstring("Start State", "Enter the start state (e.g., '1 2 3 4 5 6 7 8 0' for goal state):")
        if state:
            self.start_state = list(map(int, state.split()))
            if len(self.start_state) == 9:
                self.update_board_display(self.start_state)
            else:
                messagebox.showerror("Invalid Input", "Please enter exactly 9 numbers.")

    def solve_puzzle(self):
        # Check solvability
        if not self.is_solvable(self.start_state):
            messagebox.showinfo("Unsolvable", "The entered puzzle state is unsolvable.")
            return

        algorithm = self.algorithm_var.get()
        heuristic = self.heuristic_var.get() if algorithm == "A*" else None
        start_time = time.time()
        
        if algorithm=="A*":
            self.solution_states=Astar.Astar(self.start_state,heuristic)
    
        # Call your provided algorithm functions here, e.g., solve_with_algorithm
        # Example: self.solution_states = solve_with_algorithm(self.start_state, algorithm, heuristic)
        
        solve_time = time.time() - start_time
        messagebox.showinfo("Solution Found", f"Puzzle solved in {solve_time:.2f} seconds.")

    def is_solvable(self, state):
        # Count inversions to check if solvable
        inv_count = sum(1 for i in range(len(state)) for j in range(i + 1, len(state)) if state[i] > state[j] and state[i] and state[j])
        return inv_count % 2 == 0

    def animate_solution(self):
        # Ensure solution states are loaded
        if not self.solution_states:
            messagebox.showerror("No Solution", "Please solve the puzzle first.")
            return

        # Loop through each state in the solution sequence
        for state in self.solution_states:
            self.update_board_display(state)  # Update the display with the current state
            self.root.update()               # Update the Tkinter GUI window to show changes
            time.sleep(0.5)                  # Pause for half a second for visualization

    def update_board_display(self, state):
        # Convert the flat 1D list into the 3x3 display grid
        for i in range(self.board_size):
            for j in range(self.board_size):
                tile = state[i * self.board_size + j]   # Access the tile value from the 1D list
                self.board[i][j].config(text=str(tile) if tile != 0 else "")  # Display value, leave empty for 0

root = tk.Tk()
app = PuzzleSolverGUI(root)
root.mainloop()
