import Astar
start_state=[0,4,7,5,2,3,8,6,1]
flag=1 # euclidean
cost, current_state, path, previous_moves =Astar.Astar(start_state,flag)
print(cost)
print(current_state)
print(path)
print(previous_moves)