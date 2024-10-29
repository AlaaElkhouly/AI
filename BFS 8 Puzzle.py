from collections import deque
# Define the goal state
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Define valid moves
def get_neighbors(state):
    neighbors = []
    index_of_blank = state.index(0)  # find the blank space (0)
    row, col = index_of_blank // 3, index_of_blank % 3
    # Define the possible moves (Up, Down, Left, Right)
    moves = {
        'Up': (-1, 0),
        'Down': (1, 0),
        'Left': (0, -1),
        'Right': (0, 1)
    }
    for move, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:  # move is within bounds
            new_blank_index = new_row * 3 + new_col
            new_state = state[:]
            new_state[index_of_blank], new_state[new_blank_index] = new_state[new_blank_index], new_state[
                index_of_blank]
            neighbors.append(new_state)

    return neighbors


# BFS algorithm
def bfs(start_state):
    queue = deque([(start_state, [])])  # each element is (state, path)
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state == GOAL_STATE:
            return path

        visited.add(tuple(current_state))

        for neighbor in get_neighbors(current_state):
            if tuple(neighbor) not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None  # no solution


# Example of running BFS
initial_state = [1, 2, 5, 3, 0, 4, 6, 7, 8]
path = bfs(initial_state)

print("Path to goal:")
for step in path:
    print(step)
