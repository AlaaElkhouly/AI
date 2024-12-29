import numpy as np
import matplotlib.pyplot as plt

# Define the grid world setup and transition model
def create_grid_world(r):
    # Reward function for the grid world
    reward_function = np.full(9, -1)  # All non-terminal states have a reward of -1
    reward_function[0] = 10  # Upper-left corner terminal state
    reward_function[2] = r   # Upper-right corner terminal state

    # Transition model
    transition_model = np.zeros((9, 4, 9))  # 9 states, 4 actions (Up, Down, Left, Right)
    
    # Action indices: Up = 0, Down = 1, Left = 2, Right = 3
    # Define the state transitions, with 80% probability to go in the intended direction
    directions = [(-3, 0), (3, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for state in range(9):
        if state == 0 or state == 2:  # Terminal states
            continue
        for action in range(4):
            intended_direction = directions[action]
            intended_state = state + intended_direction[0] + intended_direction[1]
            
            # Ensure the state is within bounds (0-8) and doesn't fall off the grid
            if intended_state < 0 or intended_state >= 9:
                intended_state = state  # Wall collision, stay in the same state
            
            # 80% to move in the intended direction
            transition_model[state, action, intended_state] += 0.8

            # For the right-angle directions (10% probability each)
            for perpendicular_action in [(action + 1) % 4, (action + 3) % 4]:
                perpendicular_direction = directions[perpendicular_action]
                perpendicular_state = state + perpendicular_direction[0] + perpendicular_direction[1]

                # Ensure perpendicular state is within bounds
                if perpendicular_state < 0 or perpendicular_state >= 9:
                    perpendicular_state = state  # Wall collision, stay in the same state
                
                transition_model[state, action, perpendicular_state] += 0.1

    return reward_function, transition_model

class ValueIteration:
    def __init__(self, reward_function, transition_model, gamma, epsilon=1e-3):
        self.num_states = len(reward_function)
        self.num_actions = len(transition_model[0])  # Number of actions
        self.reward_function = np.nan_to_num(reward_function)

        self.transition_model = transition_model
        self.gamma = gamma
        self.epsilon = epsilon

        self.values = np.zeros(self.num_states)
        self.policy = np.zeros(self.num_states, dtype=int)

    def update_values(self):
        """ Update values based on Bellman equation """
        delta = 0
        new_values = np.copy(self.values)
        for s in range(self.num_states):
            if self.reward_function[s] == 10 or self.reward_function[s] == r:  # Terminal states
                continue
            v_list = np.zeros(self.num_actions)
            for a in range(self.num_actions):
                p = self.transition_model[s, a]
                v_list[a] = np.sum(p * self.values)
            new_values[s] = self.reward_function[s] + self.gamma * np.max(v_list)
            delta = max(delta, abs(self.values[s] - new_values[s]))
        self.values = new_values
        return delta

    def extract_policy(self):
        """ Extract the policy from the current values """
        for s in range(self.num_states):
            if self.reward_function[s] == 10 or self.reward_function[s] == r:  # Terminal states
                continue
            v_list = np.zeros(self.num_actions)
            for a in range(self.num_actions):
                p = self.transition_model[s, a]
                v_list[a] = np.sum(p * self.values)
            self.policy[s] = np.argmax(v_list)

    def train(self):
        epoch = 0
        delta = self.update_values()
        while delta > self.epsilon:
            epoch += 1
            delta = self.update_values()
            if epoch % 10 == 0:  # Print every 10 iterations
                print(f"\nEpoch {epoch}:")
                self.print_grid(self.values, "Values")
                self.print_grid(self.policy, "Policy")

        print(f'\nFinal Policy:')
        self.print_grid(self.policy, "Final Policy")
        print(f'Final Values:')
        self.print_grid(self.values, "Final Values")

    def print_grid(self, data, title=""):
        """ Helper function to print the grid """
        grid_size = 3  # 3x3 grid
        arrows = ['↑', '↓', '←', '→']
        grid = np.full((grid_size, grid_size), "", dtype=object)
        value_grid = np.full((grid_size, grid_size), "", dtype=object)

        for i in range(grid_size):
            for j in range(grid_size):
                idx = i * grid_size + j
                if data is self.policy:
                    grid[i, j] = arrows[data[idx]]  # Policy (actions)
                elif data is self.values:
                    value_grid[i, j] = f"{data[idx]:.2f}"  # Values

        print(f"{title} Grid:")
        for i in range(grid_size):
            print(' '.join(grid[i]))
        print("\nValues Grid:")
        for i in range(grid_size):
            print(' '.join(value_grid[i]))

# Example usage of ValueIteration
r_values = [100, 3, 0, -3]
for r in r_values:
    reward_function, transition_model = create_grid_world(r)
    value_iteration = ValueIteration(reward_function, transition_model, gamma=0.99)
    value_iteration.train()
