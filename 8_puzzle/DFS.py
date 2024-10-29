import time
import HelpingFns as c
def DFS(start_state,GOAL_STATE):
    print("Depth-First Search (DFS) Running.....")
    start_time = time.time()
    stack = [(start_state, [])]  # each element is (state, path)
    visited = set()
    while stack and time.time() <= start_time + 30:
        current_state, path = stack.pop()
        if current_state == GOAL_STATE:
            print("Path:",path)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            return path
        visited.add(tuple(current_state))
        for neighbor in c.get_neighbors(current_state):
            if tuple(neighbor) not in visited:
                stack.append((neighbor, path + [neighbor]))
    print("Sorry, no path found :(")
    return None  # no solution
