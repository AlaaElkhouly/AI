import random
import numpy as np
# Constants
grid_size = 3
discount_factor = 0.99
ACTIONS = ['↑', '↓', '→', '←']
DIRECTION_DELTAS = {'↑': -3,'↓': 3,'→': 1,'←': -1}

# takes action as an input and outputs the random action to implement
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
#_______________________________________________________________________________________________________________________________________________#
# Value Iteration
def value_iteration(rewards, discount_factor=0.99, theta=1e-6):
    values = 9*[0]  # Initialize state values
    policy = 9*['↑']  # Initialize with arbitrary actions

    while True:
        delta = 0
        new_values = np.copy(values)
        for i in range(9):
                state = i
                action_values = {}
                for action in ACTIONS:
                    d = DIRECTION_DELTAS[action]
                    next_state = state + d
                    if (next_state <0)or (next_state > 8) or(state % 3 == 0 and action == '←') or (state % 3 == 2 and action == '→'):
                        next_value = rewards[state] # Stay in place if action moves out of bounds
                    else:
                        next_value = rewards[next_state] + discount_factor * values[next_state]
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
#_______________________________________________________________________________________________________________________________________________#
# Main function
def main():
    r_values = [100, 3, 0, -3]

    for r in r_values:
        rewards =[r, -1, 10, -1, -1, -1,-1, -1, -1]
        vv, pv = value_iteration(rewards,discount_factor)

        # Convert values to integers for cleaner printing
        vv = [int(x) for x in vv]

        print(f"Value Iteration Vs Policy Iteration for r = {r}\n")
        print("Optimal Values:")
        print(vv[:3])
        print(vv[3:6])
        print(vv[6:])
        print("Optimal Policy:")
        print(pv[:3])
        print(pv[3:6])
        print(pv[6:])

if __name__ == "__main__":
    main()