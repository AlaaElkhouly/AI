import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import Astar
import BFS
import DFS
import fares_idfs

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
        self.max_depth=tk.IntVar(value=50)
        self.time_limit=30 #time limit for algorithms is 30s
        algo_frame = tk.Frame(self.root) #algorithm slelection window
        algo_frame.pack()# add to root window
        tk.Label(algo_frame, text="Select Algorithm: ").pack(side=tk.LEFT) #prompt user to choose alogrithm
        tk.OptionMenu(algo_frame, self.algorithm_var, "BFS", "DFS", "IDFS", "A*").pack(side=tk.LEFT)

        # Heuristic selection for A*
        self.heuristic_var = tk.StringVar(value="Manhattan")
        tk.Label(algo_frame, text="Heuristic: ").pack(side=tk.LEFT)
        tk.OptionMenu(algo_frame, self.heuristic_var, "Eucleadian", "Manhattan").pack(side=tk.LEFT)
        
        # Buttons to enter state, solve, and show solution
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        tk.Button(control_frame, text="Enter Start State", command=self.enter_start_state).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Solve", command=self.solve_puzzle).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Animate Solution", command=self.animate_solution).pack(side=tk.LEFT)
        tk.Button(control_frame, text="enter max depth", command=self.enter_depth).pack(side=tk.LEFT)

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
        state = simpledialog.askstring("Start State", "Enter the start state (for example '123456780' for goal state):")
    
        if state:
        # Convert the input string into a list of integers
            array = [int(digit) for digit in state]
        
        # Check if the array has exactly 9 elements and contains unique numbers from 0 to 8
            if len(array) != 9 or len(array) != len(set(array)) or any(num < 0 or num > 8 for num in array):
                messagebox.showerror("Invalid Input", "Please enter exactly 9 digits from 0 to 8.")
            else:
                self.start_state = array  # Update start_state with the valid input
                print(f"Start state: {self.start_state}")  # Debugging line
                self.update_board_display(self.start_state)  # Update the display to show the new start state

    def enter_depth(self):
        self.max_depth=simpledialog.askinteger("max depth for idfs"," enter the max depth default is 100")                

    def solve_puzzle(self):
    # Check solvability
        if not self.is_solvable(self.start_state):
            messagebox.showinfo("Unsolvable", "The entered puzzle state is unsolvable.")
            return

        algorithm = self.algorithm_var.get()
        heuristic = self.heuristic_var.get() if algorithm == "A*" else None
        max_depth = self.max_depth.get() if algorithm == "IDFS" else None
        start_time = time.time()
        

    # Run the selected algorithm with time limit
        
        while(True):
            elapsed_time = time.time() - start_time
            
            if elapsed_time >= 30:
                messagebox.showinfo("Time Limit Exceeded", "The time limit has been exceeded without finding a solution.")
                return
        
            if algorithm == "A*":
                cost, current_state, path, previous_moves, nodes_explored = Astar.Astar(self.start_state, heuristic)
                if path:
                    self.solution_states = path #if solution found
                    break

            elif algorithm == "BFS":
                current_state, path, previous_moves, nodes_explored = BFS.BFS(self.start_state)
                if path:
                    self.solution_states = path #if solution found
                    cost = len(path)
                    break

            elif algorithm == "DFS":
                current_state, path, previous_moves, nodes_explored = DFS.DFS(self.start_state)
                if path:
                    self.solution_states = path #if solution found
                    cost = len(path)
                    break

            elif algorithm == "IDFS":
                result = fares_idfs.iterative_DFS(self.start_state, max_depth)

                if result:  # Check if IDFS found a solution
                    current_state = result['path_to_goal'][-1] if result['path_to_goal'] else self.start_state
                    path = result['path_to_goal']
                    depth = result['search_depth']
                    cost = result['cost_of_path']
                    nodes_explored = result['nodes_expanded']
                    previous_moves=path
                    self.solution_states = path
                    break

        if not self.solution_states:
            messagebox.showinfo("No Solution", "No solution found within the depth limit or time limit has been exceeded.")
            return

        solve_time = time.time() - start_time
        message = (
        f"Puzzle solved in {solve_time:.5f} seconds.\n"
        f"Solution depth: {len(self.solution_states)}\n"
        f"Cost of path: {cost}\n"
        f"Nodes explored: {nodes_explored}\n"
        f"Moves made: {previous_moves}\n"
        )
        messagebox.showinfo("Solution Summary", message)

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
            time.sleep(0.1)                  # Pause for  visualization

    def update_board_display(self, state):
        print(f"Updating board display with state: {state}")  # Debugging line
    
    # Ensure that state is valid
        if not isinstance(state, list) or len(state) != 9:
            print("Error: Invalid state. Expected a list of 9 elements.")
            return
    # Convert the flat 1D list into the 3x3 display grid
        for i in range(3):  # Assuming a 3x3 puzzle
            for j in range(3):
                tile = state[i * 3 + j]   # Access the tile value from the 1D list
                self.board[i][j].config(text=str(tile) if tile != 0 else "")  # Update the display

root = tk.Tk()
app = PuzzleSolverGUI(root)
root.mainloop()
