import heapq
import math
#-------------------HELPING FUNCTIONS--------------------
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
    
    
def get_neighbors_Astar(state):
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

#-------------------------------------------------------------------------------------
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def Astar(start_state, flag):
    # Initialize the priority queue as a min-heap
    priority_queue = []
    
    # Push the initial state into the priority queue
    heapq.heappush(priority_queue, (0, start_state, [], []))  # (cost, state, path, moves)

    # Initialize a set to keep track of visited nodes
    visited = set()

    # Initialize a dictionary to store the minimum cost to reach each state
    min_cost_to_state = {tuple(start_state): 0}  # Use tuple for hashability

    # Start the algorithm sequence
    while priority_queue:
        cost, current_state, path, previous_moves = heapq.heappop(priority_queue)  # Pop the lowest cost state
        
        # Check if we have arrived at the goal
        if current_state == GOAL_STATE:
            print("Path found:", path)
            return cost, current_state, path, previous_moves
        
        visited.add(tuple(current_state))  # Add the current state to visited
        
        # Get valid neighbors and their corresponding states and moves
        neighbors, neighbor_states, new_moves = get_neighbors_Astar(current_state)
        
        # Loop through neighbors
        for neighbor, move in zip(neighbor_states, new_moves):  # Loop through resulting states
            neighbor_tuple = tuple(neighbor)
            if sorted(neighbor) == list(range(9)):
               # Calculate new cost to visit the neighbor
               new_cost = cost + 1
               total_cost = new_cost + calc_heuristic(neighbor, flag)

               # Check if the neighbor has been visited or if the new path is cheaper
               if (neighbor_tuple not in visited) or (total_cost < min_cost_to_state.get(neighbor_tuple, float('inf'))):
                  # Update the minimal cost in the dictionary
                  min_cost_to_state[neighbor_tuple] = new_cost
                  # Push the neighbor state into the priority queue
                  heapq.heappush(priority_queue, (total_cost, neighbor, path + [neighbor], previous_moves + [move]))

    # If we exit the loop without finding the goal
    print("Sorry, no path found :(")
    return 0,0,0,0