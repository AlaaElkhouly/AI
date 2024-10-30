import time
import HelpingFns as c
from collections import deque

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def BFS(start_state):
    print("Breadth-First Search (BFS) Running.....")
    start_time = time.time()
    queue = deque([(start_state, [], [])])  # each element is (state, path,previous moves)
    visited = set()
    #add counter for nodes explored
    nodes_expolred=0
    
    while queue :
        if time.time()-start_time > 30:
            break
        current_state, path, previous_moves = queue.popleft()
        nodes_expolred+=1 # increment the counter
        if current_state == GOAL_STATE:
            print("Path:",path)
            print("moves made:",previous_moves)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            print("cost (in moves):")
            return current_state, path, previous_moves,nodes_expolred
        visited.add(tuple(current_state))
        neighbor, neighbor_state, moves= c.get_neighbors(current_state)
        for state,move in zip(neighbor_state,moves)  :
                if tuple(state) not in visited:
                    queue.append((state, path + [state],previous_moves+[move]))
    print("Sorry, no path found :(")
    return None  # no solution

#EXAMPLE

##current_state, path, previous_moves,nodes_explored=BFS(start_state)