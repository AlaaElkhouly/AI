def dfs(start_state):
    stack = [(start_state, [])]  # each element is (state, path)
    visited = set()

    while stack:
        current_state, path = stack.pop()

        if current_state == GOAL_STATE:
            return path

        visited.add(tuple(current_state))

        for neighbor in get_neighbors(current_state):
            if tuple(neighbor) not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None  # no solution
