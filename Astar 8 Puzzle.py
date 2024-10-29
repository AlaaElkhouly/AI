import heapq
import math


# Heuristics
def manhattan_distance(state):
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        target_row, target_col = value // 3, value % 3
        current_row, current_col = index // 3, index % 3
        distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


def euclidean_distance(state):
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        target_row, target_col = value // 3, value % 3
        current_row, current_col = index // 3, index % 3
        distance += math.sqrt((current_row - target_row) ** 2 + (current_col - target_col) ** 2)
    return distance


# A* algorithm
def astar(start_state, heuristic):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_state, []))
    visited = set()

    while priority_queue:
        cost, current_state, path = heapq.heappop(priority_queue)

        if current_state == GOAL_STATE:
            return path

        visited.add(tuple(current_state))

        for neighbor in get_neighbors(current_state):
            if tuple(neighbor) not in visited:
                new_cost = cost + 1 + heuristic(neighbor)
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))

    return None
