import heapq
import time
import math
import HelpingFns as h
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
        if flag=="Eucleadian":
            distance += math.sqrt((current_row - target_row) ** 2 + (current_col - target_col) ** 2) # flag = 1 for eucleadian distance
        else:
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance
    
    


#-------------------------------------------------------------------------------------
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def Astar(start_state, flag):
    print("A* Running.....")
    start_time = time.time()
    # Initialize the priority queue as a min-heap
    priority_queue = []

    #add counter for nodes explored
    nodes_expolred=0
    
    # Push the initial state into the priority queue
    heapq.heappush(priority_queue, (0, start_state, [], []))  # (cost, state, path, moves)

    # Initialize a set to keep track of visited nodes
    visited = set()

    # Initialize a dictionary to store the minimum cost to reach each state
    min_cost_to_state = {tuple(start_state): 0}  # Use tuple for hashability

    # Start the algorithm sequence
    while priority_queue and time.time() <= start_time + 30:
        cost, current_state, path, previous_moves = heapq.heappop(priority_queue) # Pop the lowest cost state(b3ml sort w b3deen pop)
        nodes_expolred+=1
        # Check if we have arrived at the goal
        if current_state == GOAL_STATE:
            print("Path found:", path)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            return cost, current_state, path, previous_moves,nodes_expolred
        
        visited.add(tuple(current_state))  # Add the current state to visited
        
        # Get valid neighbors and their corresponding states and moves
        neighbors, neighbor_states, new_moves = h.get_neighbors(current_state)
        
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
    return 0,0,0,0,0

#example
#cost, current_state, path, previous_moves, nodes_expolred=Astar(start_state=,flag)