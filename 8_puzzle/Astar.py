import HelpingFns
import heapq
import RunMe
def Astar(start_state,flag):
   priority_que=[]                  #treat as a min-heap
   heapq.heappush(priority_que,(0,start_state,[])) # push into the queue a tuble containing (cost of start, start_state, path to start state)

   #initialize a lsit to keep track of visited nodes
   visited=set() #an empty set to avoid redundancy 

   #initialize a dictionary to store the min cost to reach each state
   min_cost_to_state={tuple(start_state):0} # 5alybalak must  be tuple for hashability
   
   #start algorithm sequence
   while (priority_que):
      cost,current_state,path=heapq.heappop(priority_que) # pop el value that has max priority(lowest cost)
      #check wether we arrived 
      if current_state==RunMe.GOAL_STATE:
         print("Path found:", path)
         return path
      visited.add(tuple(current_state)) # add the list of visited states
    
        #loop through neighbors
      for neighbor in HelpingFns.get_neighbors_for_Astar(current_state): # loop through all resulting states from swapping with neighbors
         neighbor_tuple=tuple(neighbor)
         
         #calculate new cost to visiting any neighbor = old cost plus one 3lshan its only one step away
         new_cost=cost +1
         total_cost= new_cost + HelpingFns.calc_heuritic(flag)

         #check if this neighbor has been already visited if not check if this new path is cheaper than the one recorded
         if(neighbor_tuple not in visited) or (total_cost<min_cost_to_state.get(neighbor_tuple,float('inf'))): # 'inf' is just a place holder
            # pupdate the new minimal cost into dictionary
            min_cost_to_state[neighbor_tuple]=new_cost
            #push the neighbor state into proiority queue and update the path o inlude the most recent changes 
            heapq.heappush(priority_que(total_cost,neighbor,path + [neighbor]))

 # If we exit the loop without finding the goal
   print("Sorry, no path found :(")
   return None

    
    
