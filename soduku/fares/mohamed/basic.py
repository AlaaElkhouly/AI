import queue

class Variable:
    def __init__(self, domain=None, value=0):
        self.value = value
        self.domain = domain if domain is not None else [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __str__(self):
        return str(self.value)

class Arc:
    def __init__(self, v1=None, v2=None):
        self.v1 = v1
        self.v2 = v2

class State:
    def __init__(self, grid):
        self.grid = grid
        self.variables = []
        self.constraints = []
        # Initialize variables based on grid input
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
                    # Row constraints
                    if j != k:
                        rowArc = (self.variables[i][j], self.variables[i][k])
                        self.constraints.append(rowArc)
                    # Column constraints
                    if i != k:
                        colArc = (self.variables[i][j], self.variables[k][j])
                        self.constraints.append(colArc)
                    # Block constraints
                    if not (i == 3 * (i // 3) + (k // 3) and j == 3 * (j // 3) + k % 3):
                        blockArc = (self.variables[i][j], self.variables[3 * (i // 3) + (k // 3)][3 * (j // 3) + k % 3])
                        self.constraints.append(blockArc)

    def get_constraints_for_variable(self, variable):
        return [arc[0] for arc in self.constraints if arc[1] == variable]

    def ac3(self):
        q = queue.Queue()
        for arc in self.constraints:
            q.put(arc)

        while not q.empty():
            Xi, Xj = q.get()
            if self.revise(Xi, Xj):
                if len(Xi.domain) == 0:
                    return False
                for Xk in self.get_constraints_for_variable(Xi):
                    if Xk != Xj:
                        q.put((Xk, Xi))
        return True

    def revise(self, Xi, Xj):
        revised = False
        for x in Xi.domain[:]:
            if all(x == y for y in Xj.domain):
                Xi.domain.remove(x)
                revised = True
        return revised

def is_valid_move(grid, row, col, num):
    # Row check
    for i in range(9):
        if grid[row][i] == num:
            return False
    # Column check
    for i in range(9):
        if grid[i][col] == num:
            return False
    # 3x3 block check
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
            state.grid[row][col] = 0  # Undo move
            state.variables[row][col] = Variable()
    return False

def print_values(state):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(state.variables[i][j])
            else:
                print(str(state.variables[i][j]) + " ", end=" ")

if __name__ == '__main__':
    grid = [
        [0, 7, 0, 0, 0, 0, 6, 8, 0],
        [0, 0, 0, 0, 7, 3, 0, 0, 9],
        [3, 0, 9, 0, 0, 0, 0, 4, 5],
        [4, 9, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 3, 6],
        [9, 6, 0, 0, 0, 0, 3, 0, 8],
        [7, 0, 0, 6, 8, 0, 0, 0, 0],
        [0, 2, 8, 0, 0, 0, 6, 8, 0],
    ]

    sudoku_state = State(grid)
    print("Sudoku Board Before Solving:")
    print_values(sudoku_state)
    print("\nSolving Sudoku...\n")

    if backtracking_solver(sudoku_state):
        print("Solved Sudoku Board:")
        print_values(sudoku_state)
    else:
        print("No solution exists for this Sudoku.")
