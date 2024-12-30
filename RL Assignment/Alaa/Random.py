import numpy as np
# Constants
grid_size = 3
discount_factor = 0.99
ACTIONS = ['↑', '↓', '→', '←']
DIRECTION_DELTAS = {'↑': -3, '↓': 3, '→': 1, '←': -1}

# Function to calculate next_value with stochasticity
def calculate_stochastic_value(state, action, rewards, values, discount_factor):
    intended_delta = DIRECTION_DELTAS[action]
    perpendicular_deltas = [
        DIRECTION_DELTAS[ACTIONS[(ACTIONS.index(action) - 1) % 4]],  # Left of action
        DIRECTION_DELTAS[ACTIONS[(ACTIONS.index(action) + 1) % 4]],  # Right of action
    ]

    # Define probabilities
    probabilities = [0.8, 0.1, 0.1]
    deltas = [intended_delta] + perpendicular_deltas

    next_value = 0
    for prob, delta in zip(probabilities, deltas):
        next_state = state + delta
        # Handle grid boundaries and invalid transitions
        if next_state < 0 or next_state >= 9 or \
           (state % 3 == 0 and delta == -1) or \
           (state % 3 == 2 and delta == 1):
            next_value += prob * (rewards[state] + discount_factor * values[state])  # Stay in place
        else:
            next_value += prob * (rewards[next_state] + discount_factor * values[next_state])
    return next_value

# Value Iteration
def value_iteration(rewards, discount_factor=0.99, theta=1e-6):
    values = 9 * [0]  # Initialize state values
    policy = 9 * ['↑']  # Initialize with random actions

    while True:
        delta = 0
        new_values = np.copy(values)
        for i in range(9):
            state = i
            action_values = {}
            for action in ACTIONS:
                next_value = calculate_stochastic_value(state, action, rewards, values, discount_factor)
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

# Policy Iteration
def policy_iteration(rewards, discount_factor=0.99, theta=1e-6):
    values = 9 * [0]  # Initialize with arbitrary values
    policy = 9 * ['↑']  # Initialize policy with default actions

    def evaluate_policy():
        while True:
            delta = 0
            new_values = np.copy(values)
            for i in range(9):
                state = i
                action = policy[state]  # Current action under the policy
                next_value = calculate_stochastic_value(state, action, rewards, values, discount_factor)
                new_values[state] = next_value
                delta = max(delta, abs(values[state] - new_values[state]))
            values[:] = new_values
            if delta < theta:
                break

    def improve_policy():
        stable = True
        for i in range(9):
            state = i
            old_action = policy[state]
            action_values = {}
            for action in ACTIONS:
                next_value = calculate_stochastic_value(state, action, rewards, values, discount_factor)
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

# Main function
def main():
    r_values = [100, 3, 0, -3]

    for r in r_values:
        rewards = [r, -1, 10, -1, -1, -1, -1, -1, -1]

        vp, pp = policy_iteration(rewards, discount_factor)
        vv, pv = value_iteration(rewards, discount_factor)

        # Convert values to integers for cleaner printing
        vp = [int(x) for x in vp]
        vv = [int(x) for x in vv]

        print(f"Value Iteration Vs Policy Iteration for r = {r}\n")
        print("Optimal Values:")
        print(vv[:3], "   ", vp[:3])
        print(vv[3:6], "   ", vp[3:6])
        print(vv[6:], "   ", vp[6:], '\n')
        print("Optimal Policy:")
        print(pv[:3], "   ", pp[:3])
        print(pv[3:6], "   ", pp[3:6])
        print(pv[6:], "   ", pp[6:], "\n")

if __name__ == "__main__":
    main()
