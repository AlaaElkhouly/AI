import numpy as np

# Define the 3x3 world
world_size = 3
actions = ['U', 'D', 'L', 'R']
action_probabilities = [0.8, 0.1, 0.1]  # Probabilities for intended direction and right angles

# Define the transition model
def transition_model(state, action):
    x, y = state
    if action == 'U':
        return [(max(x-1, 0), y), (x, max(y-1, 0)), (x, min(y+1, world_size-1))]
    elif action == 'D':
        return [(min(x+1, world_size-1), y), (x, max(y-1, 0)), (x, min(y+1, world_size-1))]
    elif action == 'L':
        return [(x, max(y-1, 0)), (max(x-1, 0), y), (min(x+1, world_size-1), y)]
    elif action == 'R':
        return [(x, min(y+1, world_size-1)), (max(x-1, 0), y), (min(x+1, world_size-1), y)]

# Define the reward function
def reward(state):
    if state == (0, 0):
        return 100
    elif state == (2, 2):
        return -100
    else:
        return -1

# Define the value iteration algorithm
def value_iteration(r, discount_factor=0.99, theta=0.0001):
    V = np.zeros((world_size, world_size))
    policy = np.full((world_size, world_size), ' ')
    
    while True:
        delta = 0
        for x in range(world_size):
            for y in range(world_size):
                v = V[x, y]
                max_value = float('-inf')
                best_action = None
                
                for action in actions:
                    new_states = transition_model((x, y), action)
                    value = sum(action_probabilities[i] * (reward(new_states[i]) + discount_factor * V[new_states[i]]) for i in range(3))
                    
                    if value > max_value:
                        max_value = value
                        best_action = action
                
                V[x, y] = max_value
                policy[x, y] = best_action
                delta = max(delta, abs(v - V[x, y]))
        
        if delta < theta:
            break
    
    return policy

# Define the policy iteration algorithm
def policy_iteration(r, discount_factor=0.99, theta=0.0001):  # Added theta parameter here
    policy = np.random.choice(actions, size=(world_size, world_size))
    V = np.zeros((world_size, world_size))
    
    while True:
        # Policy evaluation
        while True:
            delta = 0
            for x in range(world_size):
                for y in range(world_size):
                    v = V[x, y]
                    new_states = transition_model((x, y), policy[x, y])
                    V[x, y] = sum(action_probabilities[i] * (reward(new_states[i]) + discount_factor * V[new_states[i]]) for i in range(3))
                    delta = max(delta, abs(v - V[x, y]))
            
            if delta < theta:
                break
        
        # Policy improvement
        policy_stable = True
        for x in range(world_size):
            for y in range(world_size):
                old_action = policy[x, y]
                max_value = float('-inf')
                best_action = None
                
                for action in actions:
                    new_states = transition_model((x, y), action)
                    value = sum(action_probabilities[i] * (reward(new_states[i]) + discount_factor * V[new_states[i]]) for i in range(3))
                    
                    if value > max_value:
                        max_value = value
                        best_action = action
                
                policy[x, y] = best_action
                
                if old_action != best_action:
                    policy_stable = False
        
        if policy_stable:
            break
    
    return policy

# Values of r to test
r_values = [100, 3, 0, -3]

# Perform value iteration and policy iteration for each value of r
for r in r_values:
    print(f"Value Iteration Policy for r={r}:")
    vi_policy = value_iteration(r)
    print(vi_policy)
    
    print(f"Policy Iteration Policy for r={r}:")
    pi_policy = policy_iteration(r)
    print(pi_policy)
