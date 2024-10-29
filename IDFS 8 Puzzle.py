def dls(state, depth, visited, path):
    if state == GOAL_STATE:
        return path

    if depth <= 0:
        return None

    visited.add(tuple(state))

    for neighbor in get_neighbors(state):
        if tuple(neighbor) not in visited:
            result = dls(neighbor, depth - 1, visited, path + [neighbor])
            if result is not None:
                return result

    return None


def iddfs(start_state, max_depth):
    for depth in range(max_depth):
        visited = set()
        result = dls(start_state, depth, visited, [])
        if result is not None:
            return result
    return None
