import numpy as np
# Constants
GRID_SIZE = 3
DISCOUNT_FACTOR = 0.9
ACTIONS = ['Up', 'Down', 'Right', 'Left']
ACTION_PROBABILITIES = {
    'intended': 0.8,  # Probability of moving in the intended direction
    'right_angle': 0.1  # Probability of moving at a right angle
}

# Rewards for the grid
def create_rewards(r):
    return np.array([
        [r, -1, 10],
        [-1, -1, -1],
        [-1, -1, -1]
    ])

# Transition model
DIRECTION_DELTAS = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Right': (0, 1),
    'Left': (0, -1)
}

def is_valid_position(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

def transition_probabilities(state, action):
    x, y = state
    transitions = []

    # Intended move
    intended_delta = DIRECTION_DELTAS[action]
    intended_pos = (x + intended_delta[0], y + intended_delta[1])
    if is_valid_position(*intended_pos):
        transitions.append((intended_pos, ACTION_PROBABILITIES['intended']))
    else:
        transitions.append(((x, y), ACTION_PROBABILITIES['intended']))

    # Right-angle moves
    for right_angle_action in [a for a in ACTIONS if a != action]:
        right_angle_delta = DIRECTION_DELTAS[right_angle_action]
        right_angle_pos = (x + right_angle_delta[0], y + right_angle_delta[1])
        if is_valid_position(*right_angle_pos):
            transitions.append((right_angle_pos, ACTION_PROBABILITIES['right_angle']))
        else:
            transitions.append(((x, y), ACTION_PROBABILITIES['right_angle']))

    return transitions

# Value Iteration
def value_iteration(rewards, threshold=1e-4):
    values = np.zeros((GRID_SIZE, GRID_SIZE))  # Initialize all state values to zero
    policy = np.full((GRID_SIZE, GRID_SIZE), '', dtype=object)  # To store optimal policy

    while True:
        delta = 0  # Track the maximum value change
        new_values = np.copy(values)  # Copy the current value table

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                state = (x, y)
                action_values = []

                for action in ACTIONS:
                    action_value = 0
                    for next_state, prob in transition_probabilities(state, action):
                        next_x, next_y = next_state
                        action_value += prob * (rewards[next_x, next_y] + DISCOUNT_FACTOR * values[next_x, next_y])
                    action_values.append(action_value)

                # Update the value of the state
                new_values[x, y] = max(action_values)

                # Update the policy to the action with the highest value
                policy[x, y] = ACTIONS[np.argmax(action_values)]

                # Update the delta
                delta = max(delta, abs(new_values[x, y] - values[x, y]))

        values = new_values

        # Check for convergence
        if delta < threshold:
            break

    return values, policy

# Policy Iteration
def policy_iteration(rewards, threshold=1e-4):
    policy = np.random.choice(ACTIONS, size=(GRID_SIZE, GRID_SIZE))  # Start with a random policy
    values = np.zeros((GRID_SIZE, GRID_SIZE))  # Initialize state values to zero

    while True:
        # Policy Evaluation
        while True:
            delta = 0
            new_values = np.copy(values)

            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    state = (x, y)
                    action = policy[x, y]
                    action_value = 0

                    for next_state, prob in transition_probabilities(state, action):
                        next_x, next_y = next_state
                        action_value += prob * (rewards[next_x, next_y] + DISCOUNT_FACTOR * values[next_x, next_y])

                    new_values[x, y] = action_value
                    delta = max(delta, abs(new_values[x, y] - values[x, y]))

            values = new_values

            if delta < threshold:
                break

        # Policy Improvement
        policy_stable = True

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                state = (x, y)
                old_action = policy[x, y]
                action_values = []

                for action in ACTIONS:
                    action_value = 0
                    for next_state, prob in transition_probabilities(state, action):
                        next_x, next_y = next_state
                        action_value += prob * (rewards[next_x, next_y] + DISCOUNT_FACTOR * values[next_x, next_y])
                    action_values.append(action_value)

                policy[x, y] = ACTIONS[np.argmax(action_values)]

                if old_action != policy[x, y]:
                    policy_stable = False

        if policy_stable:
            break

    return values, policy

# Main function
def main():
    r_values = [100, 3, 0, -3]

    for r in r_values:
        print(f"\nValue Iteration for r = {r}")
        rewards = create_rewards(r)
        values, policy = value_iteration(rewards)

        print("Optimal Values:")
        print(values)

        print("Optimal Policy:")
        for row in policy:
            print(row)

        print(f"\nPolicy Iteration for r = {r}")
        values, policy = policy_iteration(rewards)

        print("Optimal Values:")
        print(values)

        print("Optimal Policy:")
        for row in policy:
            print(row)

if __name__ == "__main__":
    main()
