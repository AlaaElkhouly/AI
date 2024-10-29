import HelpingFns
import heapq
def Astar(start_state, heuristic):
    print("A* Search Running.....")
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_state, []))
    visited = set()
    while priority_queue:
        cost, current_state, path = heapq.heappop(priority_queue)
        if current_state == HelpingFns.GOAL_STATE:
            print("Path:",path)
            return path
        visited.add(tuple(current_state))
        for neighbor in HelpingFns.get_neighbors(current_state):
            if tuple(neighbor) not in visited:
                new_cost = cost + 1 + heuristic(neighbor)
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
    print("Sorry, no path found :(")
    return None
