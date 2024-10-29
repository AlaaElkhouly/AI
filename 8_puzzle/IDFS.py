def DLS(state, depth, visited, path):
    if state == GOAL_STATE:
        return path
    if depth <= 0:
        return None
    visited.add(tuple(state))
    for neighbor in get_neighbors(state):
        if tuple(neighbor) not in visited:
            result = DLS(neighbor, depth - 1, visited, path + [neighbor])
            if result is not None:
                return result
    return None
# ----------------------------------------------------------------------------------------------------
def IDFS(start_state, max_depth):
    print("Iterative Deepening Search (IDS) Running.....")
    for depth in range(max_depth):
        visited = set()
        result = DLS(start_state, depth, visited, [])
        if result is not None:
            print("Path:",result)
            return result
    print("Sorry, no path found :(")
    return None
