import time

MOVES = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
goal_state = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

def depth_first_search(initial_state, max_depth):
    frontier = [(initial_state, [])]
    explored = set()
    nodes_expanded = 0
    start_time = time.time()

    while frontier:
        state, path = frontier.pop()
        nodes_expanded += 1

        if state == goal_state:
            end_time = time.time()
            return {
                'path_to_goal': path,
                'cost_of_path': len(path),
                'nodes_expanded': nodes_expanded,
                'search_depth': len(path),
                'running_time': end_time - start_time
            }

        explored.add(state)

        if len(path) < max_depth:
            for r in range(3):
                for c in range(3):
                    if state[r][c] == 0:
                        row, col = r, c

            for move, (dr, dc) in MOVES.items():
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_state = list(map(list, state))
                    new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                    new_state = tuple(map(tuple, new_state))

                    if new_state not in explored and all(new_state != s for s, p in frontier):
                        frontier.append((new_state, path + [move]))
    return None



def iterative_DFS(initial_state,max_depth):
    start_time = time.time()
    for depth in range(max_depth + 1):
        result = depth_first_search(initial_state, goal_state, depth)
        if result:
            end_time = time.time()
            result['running_time'] = end_time - start_time
            path= result['path_to_goal']
            cost= result['cost_of_path']
            nodes_expanded= result['nodes_expanded']
            depth= result['search_depth']
            return path[-1],path,depth,cost,nodes_expanded
    return 


