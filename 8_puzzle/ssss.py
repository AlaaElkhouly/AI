
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
