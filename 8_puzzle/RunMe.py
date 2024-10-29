from collections import deque
import heapq
import math
import time



GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print("Please enter 9 elements (0 to 8) for the 8-puzzle game initial state:")
INITIAL_STATE=input_array()
if is_solvable(INITIAL_STATE):
    x=method_choice()
    if x==1:
        BFS(INITIAL_STATE)
    elif x==2:
        DFS(INITIAL_STATE)
    elif x==3:
        MAX_DEPTH=int(input(f"please enter max depth:\n"))
        IDFS(INITIAL_STATE,MAX_DEPTH)
    else:
        Astar(INITIAL_STATE)
else:
    print("The Puzzle you have entered is unsolvable")
