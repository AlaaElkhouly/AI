import time
import HelpingFns as c
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def IDFS(start_state, max_depth=10):
    print("Iterative Deepening Depth-First Search (IDFS) Running.....")
    explored_nodes=0
    start_time = time.time()
    def DLS(state, path, previous_moves, depth_limit):
        # Depth-Limited Search (DLS) within the current depth limit
        stack = [(state, path, previous_moves, 0)]  # each element: (state, path, previous moves, depth)
        visited = set()
        while stack and time.time() <= start_time + 30:
            current_state, path, previous_moves, depth = stack.pop()
            explored_nodes+=1
            if current_state == GOAL_STATE:
                print("Path:", path)
                print("Moves made:", previous_moves)
                print(f"Time taken: {round(time.time() - start_time, 5)} seconds")
                return current_state, path, previous_moves,explored_nodes
            if depth <= depth_limit:
                visited.add(tuple(current_state))
                neighbors, neighbor_states, moves = c.get_neighbors(current_state)
                for state, move in zip(neighbor_states, moves):
                    if tuple(state) not in visited:
                        stack.append((state, path + [state], previous_moves + [move], depth + 1))
        return None
    # Iteratively increase the depth limit and perform DLS at each level
    for depth_limit in range(max_depth + 1):
        print(f"Searching with depth limit: {depth_limit}")
        result = DLS(start_state, [], [], depth_limit)
        if result is not None:
            return result
    print("Sorry, no path found :(")
    return None  # No solution found within max depth limit
