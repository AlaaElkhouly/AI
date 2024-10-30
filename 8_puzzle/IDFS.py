import time
import HelpingFns as c
import time
import HelpingFns as c
GOAL_STATE=[0,1,2,3,4,5,6,7,8]
def IDFS(start_state, max_depth):
    print("Iterative Deepening Search (IDS) Running.....")
    start_time = time.time()
    def DLS(state, depth, visited, path):
        if state == GOAL_STATE:
            return path
        if depth <= 0:
            return None
        visited.add(tuple(state))
        for neighbor in c.get_neighbors(state):
            if tuple(neighbor) not in visited:
                result = DLS(neighbor, depth - 1, visited, path + [neighbor])
                if result is not None:
                    return result
        return None

    for depth in range(max_depth):
        visited = set()
        result = DLS(start_state, depth, visited, [])
        if result is not None:
            print("Path:", result)
            print(f"Time taken: {round(time.time() - start_time, 5)} seconds")
            return result
    
    print("Sorry, no path found :(")
    return None

def DLS(state, depth, visited, path,GOAL_STATE):
    if state == GOAL_STATE:
        return path
    if depth <= 0:
        return None
    visited.add(tuple(state))
    for neighbor in c.get_neighbors(state):
        if tuple(neighbor) not in visited:
            result = DLS(neighbor, depth - 1, visited, path + [neighbor])
            if result is not None:
                return result
    return None

def IDFS(start_state, GOAL_STATE, max_depth):
    print("Iterative Deepening Search (IDS) Running.....")
    start_time = time.time()
    for depth in range(max_depth):
        visited = set()
        result = DLS(start_state, depth, visited, [],GOAL_STATE)
        if result is not None:
            print("Path:",result)
            print(f"Time taken: {round(time.time() - start_time,5)} seconds")
            return result
    print("Sorry, no path found :(")
    return None



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