import time
import HelpingFns as c
from collections import deque

def BFS(start_state,GOAL_STATE):
    print("Breadth-First Search (BFS) Running.....")
    start_time = time.time()
    queue = deque([(start_state, [])])  # each element is (state, path)
    visited = set()
    while queue and time.time() <= start_time + 30:
        current_state, path = queue.popleft()
        if current_state == GOAL_STATE:
            print("Path:",path)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            return path
        visited.add(tuple(current_state))
        for neighbor in c.get_neighbors(current_state):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    print("Sorry, no path found :(")
    return None  # no solution