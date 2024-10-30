import Astar
# Example starting state for the 8-puzzle
# 1 2 3
# 4 5 6
# 7 8 0  --> where 0 represents the empty tile
start_state = [1, 2, 3, 
               4, 5, 6, 
               7, 8, 0]

# Choose the heuristic flag: "Euclidean" or "Manhattan"
flag = "Manhattan"  # Manhattan distance heuristic

# Call the Astar function
cost, current_state, path, previous_moves, nodes_explored = Astar.Astar(start_state=start_state, flag=flag)

# Display results
print("Cost:", cost)
print("Final State:", current_state)
print("Path to Solution:", path)
print("Moves:", previous_moves)
print("Nodes Explored:", nodes_explored)

