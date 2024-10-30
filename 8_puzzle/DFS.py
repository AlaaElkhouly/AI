import time
import HelpingFns as c
def DFS(start_state,GOAL_STATE):
    print("Depth-First Search (DFS) Running.....")
    start_time = time.time()
    stack = [(start_state, [], [])]  # each element is (state, path, previous moves)
    visited = set()
    while stack and time.time() <= start_time + 30:
        current_state, path, previous_moves= stack.pop()
        if current_state == GOAL_STATE:
            cost=len(path)
            print("Path:",path)
            print("moves made:",previous_moves)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            print("cost (in moves):",cost)
            return current_state, path, previous_moves,cost
        visited.add(tuple(current_state))
        neighbor, neighbor_state, moves= c.get_neighbors(current_state)
        for state,move in zip(neighbor_state,moves):
            if tuple(state) not in visited:
                stack.append((state, path + [state],previous_moves+[move]))
    print("Sorry, no path found :(")
    return None  # no solution
