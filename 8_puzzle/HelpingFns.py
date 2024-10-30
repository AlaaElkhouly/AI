import math

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
# Heuristic
def calc_heuristic(state,flag):
    '''
    state(list)
    flag(BOOl) 3lshan a3raf use which heuristic
    '''
    distance = 0
   
    for index, value in enumerate(state):
        if value == 0:
            continue
        target_row, target_col = value // 3, value % 3
        current_row, current_col = index // 3, index % 3
        if flag:
            distance += math.sqrt((current_row - target_row) ** 2 + (current_col - target_col) ** 2) # flag = 1 for eucleadian distance
        else:
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance
    
def get_neighbors(state):
    neighbors = []
    neighbor_states=[]
    moves_made=[]
    index_of_blank = state.index(0)  # bta5od list of states[1,2,5,3,....] w b3deen get the index of 0 (blank space)
    row, col = index_of_blank // 3, index_of_blank % 3 

    # Dectionary of all possible moves
    moves = {                                                       #c1 c2  c3
                                                                    #[0, 1, 2]   <-- Row 0
                                                                    #[3, 4, 5]   <-- Row 1
                                                                    #[6, 7, 8]   <-- Row 2#
        'Up': (-1, 0), # reduce the row index by one 
        'Down': (1, 0), # increse the row index by one 
        'Left': (0, -1), # reduce the coumn index by one 
        'Right': (0, 1)  # increse the column index by one 
    }
    for move_name,(row_change,column_change) in moves.items():
        new_row, new_col = row + row_change, col + column_change #apply changes to blank

        if 0 <= new_row < 3 and 0 <= new_col < 3:  # check that we are within board bounds
            neighbors.append([new_row,new_col]) #store the neighbor
            moves_made.append(move_name)# store the move 
            new_blank_index = new_row * 3 + new_col # acquire new index
            new_state = state[:]
            new_state[index_of_blank], new_state[new_blank_index] = new_state[new_blank_index], new_state[index_of_blank] #swapping with adjacent
            neighbor_states.append(new_state) # append the resulting state 
    return neighbors, neighbor_states, moves_made