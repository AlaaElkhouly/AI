from collections import deque
import heapq
import math
import time
import Astar as a
import BFS as b
import HelpingFns as c
import DFS as d
import IDFS as i
GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
INITIAL_STATE=c.input_array()
if c.is_solvable(INITIAL_STATE):
    x=c.method_choice()
    if x==1:
        b.BFS(INITIAL_STATE,GOAL_STATE)
    elif x==2:
        d.DFS(INITIAL_STATE,GOAL_STATE)
    elif x==3:
        MAX_DEPTH=int(input(f"please enter max depth:\n"))
        i.IDFS(INITIAL_STATE,)
    else:
        flag=int(input("enter 1 for euclidean or zero for manhattan"))
        a.Astar(INITIAL_STATE,flag)
else:
    print("The Puzzle you have entered is unsolvable")

