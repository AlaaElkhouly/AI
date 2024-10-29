def input_array():
    while True: #user will keep re-entering till array is correct
        array= []
        for i in range(9):
            element = int(input(f"Enter element {i+1}: "))
            array.append(element)
        if len(set(array))!=len(array): #checking the array has each number written once
            print("Puzzle has duplicate numbers please re-enter")
        elif max(array) != 8 or min(array) != 0 : # checking the numbers range from 0(empty) to 8
            print("puzzle numbers range from 0 to 8 please re-enter")
        else:
            print("puzzle array Entered:", array)
            break
    return array
#----------------------------------------------------------------------------------------------------
def is_solvable(state):
    #remove the blank (0)
    flat_state = [num for num in state if num != 0]
    inversions = 0
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
    return inversions % 2 == 0 # returns 0 if not solvable (odd number of inversions) and returns 1 if solvable(even number of inversions)
# ----------------------------------------------------------------------------------------------------
def method_choice():
    while True:#user will keep re-entering till number is between 1 and 4
        x=int(input("Please enter a Number from 1 to 4 to pick your method:\n1.BFS\n2.DFS\n3.iterative DFS\n4.A*\n"))
        if x<1 or x>4:
            print("Options are from 1 to 4 only!")
        else:
            break
    return x
#----------------------------------------------------------------------------------------------------
def get_neighbors(state):
    neighbors = []
    index_of_blank = state.index(0)  # find the blank space (0)
    row, col = index_of_blank // 3, index_of_blank % 3
    # Define the possible moves (Up, Down, Left, Right)
    moves = {
        'Up': (-1, 0),
        'Down': (1, 0),
        'Left': (0, -1),
        'Right': (0, 1)
    }
    for move, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:  # move is within bounds
            new_blank_index = new_row * 3 + new_col
            new_state = state[:]
            new_state[index_of_blank], new_state[new_blank_index] = new_state[new_blank_index], new_state[
                index_of_blank]
            neighbors.append(new_state)
    return neighbors
# ----------------------------------------------------------------------------------------------------
# Heuristic
def manhattan_distance(state):
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        target_row, target_col = value // 3, value % 3
        current_row, current_col = index // 3, index % 3
        distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance
# ----------------------------------------------------------------------------------------------------
# Heuristic
def euclidean_distance(state):
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        target_row, target_col = value // 3, value % 3
        current_row, current_col = index // 3, index % 3
        distance += math.sqrt((current_row - target_row) ** 2 + (current_col - target_col) ** 2)
    return distance
# ----------------------------------------------------------------------------------------------------
