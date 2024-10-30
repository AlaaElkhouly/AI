import time

MOVES = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
goal_state = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

def depth_first_search(initial_state, max_depth):
    # Ensure initial_state is in tuple of tuples format
    if isinstance(initial_state, list):
        initial_state = tuple(tuple(initial_state[i:i+3]) for i in range(0, 9, 3))

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
            # Locate the empty tile (0) in the current state
            row, col = None, None
            for r in range(3):
                for c in range(3):
                    if state[r][c] == 0:
                        row, col = r, c
                        break
                if row is not None:
                    break

            # Generate possible moves
            for move, (dr, dc) in MOVES.items():
                new_row, new_col = row + dr, col + dc

                # Check boundaries
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_state = [list(row) for row in state]  # Convert tuples to mutable list
                    new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                    new_state = tuple(tuple(row) for row in new_state)  # Convert back to tuple of tuples

                    if new_state not in explored and all(new_state != s for s, _ in frontier):
                        frontier.append((new_state, path + [move]))

    return None

def iterative_DFS(initial_state, max_depth):
    # Ensure initial_state is in tuple of tuples format
    initial_state = tuple(tuple(initial_state[i:i+3]) for i in range(0, 9, 3))
    start_time = time.time()

    for depth in range(int(max_depth) + 1):
        result = depth_first_search(initial_state, depth)
        if result:
            end_time = time.time()
            result['running_time'] = end_time - start_time
            return result

    return None

# Running the algorithm with an initial state
result = iterative_DFS([1, 0, 2, 3, 4, 5, 6, 7, 8], 100)
if result:
    print("Path to goal:", result['path_to_goal'])
    print("Cost of path:", result['cost_of_path'])
    print("Nodes expanded:", result['nodes_expanded'])
    print("Search depth:", result['search_depth'])
    print("Running time:", result['running_time'])
else:
    print("No solution found within the depth limit.")
