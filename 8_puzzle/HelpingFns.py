import math

def input_array():
    n=int(input("enter the starting board states (1-8)"))
    INITIAL_STATE=[int(digit) for digit in str(n)]
    while 9 in INITIAL_STATE or len(INITIAL_STATE)!=9 or len(INITIAL_STATE)!=len(set(INITIAL_STATE)):
       n=int(input("enter the starting board states (1-8)"))
       INITIAL_STATE=[int(digit) for digit in str(n)]
    print(INITIAL_STATE)
    return INITIAL_STATE

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