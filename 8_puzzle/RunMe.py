from collections import deque
import heapq
import math
import time
import Astar as a
import BFS as b
import HelpingFns as c
import DFS as d
import fares_idfs

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
INITIAL_STATE=c.input_array()
if c.is_solvable(INITIAL_STATE):
    x=c.method_choice()
    if x==1:
        b.BFS(INITIAL_STATE)
    elif x==2:
        d.DFS(INITIAL_STATE)
    elif x==3:
        MAX_DEPTH=int(input(f"please enter max depth:\n"))
        fares_idfs.iterative_DFS(INITIAL_STATE,MAX_DEPTH)
    else:
        flag=input("enter Euclidean or Manhattan")
        a.Astar(INITIAL_STATE,flag)
else:
    print("The Puzzle you have entered is unsolvable")

