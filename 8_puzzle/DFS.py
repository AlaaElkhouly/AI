import time
import HelpingFns as c


GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def DFS(start_state):
    print("Depth-First Search (DFS) Running.....")
    start_time = time.time()
    stack = [(start_state, [], [])]  # each element is (state, path, previous moves)
    visited = set()
    nodes_explored=0
    while stack :
        if time.time()-start_time > 30:
            break
        current_state, path, previous_moves= stack.pop()
        nodes_explored+=1
        if current_state == GOAL_STATE:
            cost=len(path)
            print("Path:",path)
            print("moves made:",previous_moves)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            return current_state, path, previous_moves,nodes_explored
        visited.add(tuple(current_state))
        neighbor, neighbor_state, moves= c.get_neighbors(current_state)
        for state,move in zip(neighbor_state,moves):
            if tuple(state) not in visited:
                stack.append((state, path + [state],previous_moves+[move]))
    print("Sorry, no path found :(")
    return 2 # no solution
