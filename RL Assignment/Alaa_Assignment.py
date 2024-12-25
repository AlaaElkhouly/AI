#WORKS BUT WITHOUT PROBABILITY#
import random
import numpy as np
# Transition model
ACTIONS = ['↑', '↓', '→', '←']
DIRECTION_DELTAS = {'↑': (-1, 0),'↓': (1, 0),'→': (0, 1),'←': (0, -1)}

def probability(intended):
    if intended in ['↑', '↓']:
        right1, right2 = '→', '←'
    else:
        right1, right2 = '↑', '↓'
    rand = random.uniform(0, 1)
    if rand < 0.8:
        return intended
    elif rand < 0.9:
        return right1
    else:
        return right2

def next_step_with_prob(current, intended):
    next_action = probability(intended)
    dx, dy = DIRECTION_DELTAS[next_action]
    x, y = current
    next = (x + dx, y + dy)
    if 0 <= next[0] < grid_size and 0 <= next[1] < grid_size:
        return next
    else:
        return current

#_________________________________________________________________________________________________________#
# Policy Iteration
def policy_iteration(rewards, discount_factor=0.99, theta=1e-6):
    grid_shape = rewards.shape
    policy = np.full(grid_shape, '↑', dtype=object)  # Initialize with arbitrary policy
    values = np.zeros(grid_shape)  # Initialize state values

    def evaluate_policy():
        while True:
            delta = 0
            new_values = np.copy(values)
            for i in range(grid_shape[0]):
                for j in range(grid_shape[1]):
                    state = (i, j)
                    action = policy[state]  # Current action under the policy
                    dx, dy = DIRECTION_DELTAS[action]
                    next_state = (state[0] + dx, state[1] + dy)
                    
                    if 0 <= next_state[0] < grid_size and 0 <= next_state[1] < grid_size:
                        next_value = rewards[next_state] + discount_factor * values[next_state]
                    else:
                        next_value = rewards[state]  # Stay in the same state if out of bounds
                    
                    new_values[state] = next_value
                    delta = max(delta, abs(values[state] - new_values[state]))
            values[:] = new_values
            if delta < theta:
                break

    def improve_policy():
        stable = True
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                state = (i, j)
                old_action = policy[state]
                action_values = {}
                for action in ACTIONS:
                    dx, dy = DIRECTION_DELTAS[action]
                    next_state = (state[0] + dx, state[1] + dy)
                    if 0 <= next_state[0] < grid_size and 0 <= next_state[1] < grid_size:
                        next_value = rewards[next_state] + discount_factor * values[next_state]
                    else:
                        next_value = rewards[state]  # Stay in the same state if out of bounds
                    action_values[action] = next_value
                best_action = max(action_values, key=action_values.get)
                policy[state] = best_action
                if best_action != old_action:
                    stable = False
        return stable

    while True:
        evaluate_policy()
        if improve_policy():
            break

    return values, policy

#_________________________________________________________________________________________________________#
# Value Iteration
def value_iteration(rewards, discount_factor=0.99, theta=1e-6):
    grid_shape = rewards.shape
    values = np.zeros(grid_shape)  # Initialize state values
    policy = np.full(grid_shape, '↑', dtype=object)  # Initialize with arbitrary actions

    while True:
        delta = 0
        new_values = np.copy(values)
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                state = (i, j)
                action_values = {}
                for action in ACTIONS:
                    dx, dy = DIRECTION_DELTAS[action]
                    next_state = (state[0] + dx, state[1] + dy)
                    if 0 <= next_state[0] < grid_size and 0 <= next_state[1] < grid_size:
                        next_value = rewards[next_state] + discount_factor * values[next_state]
                    else:
                        next_value = rewards[state]  # Stay in the same state if out of bounds
                    action_values[action] = next_value
                # Find the maximum value and update
                best_action = max(action_values, key=action_values.get)
                new_values[state] = action_values[best_action]
                policy[state] = best_action
                delta = max(delta, abs(values[state] - new_values[state]))
        values[:] = new_values
        if delta < theta:
            break

    return values, policy
#_________________________________________________________________________________________________________#
# Constants
grid_size = 3
discount_factor = 0.99

# Main function
def main():
    r_values = [100, 3, 0, -3]

    for r in r_values:
        rewards = np.array([[r, -1, 10],[-1, -1, -1],[-1, -1, -1]])

        print(f"\nValue Iteration for r = {r}")
        values, policy = value_iteration(rewards,discount_factor)

        print("Optimal Values:")
        print(values)

        print("Optimal Policy:")
        for row in policy:
            print(row)

        print(f"\nPolicy Iteration for r = {r}")
        values, policy = policy_iteration(rewards,discount_factor)

        print("Optimal Values:")
        print(values)

        print("Optimal Policy:")
        for row in policy:
            print(row)

if __name__ == "__main__":
    main()