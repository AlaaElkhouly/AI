import numpy as np

class GridWorldSolver:
    def __init__(self, r, discount_factor=0.99):
        self.size = 3  # Fixed 3x3 grid
        self.r = r  # Reward for upper-left terminal state
        self.discount_factor = discount_factor

        # Initialize rewards: -1 for all states except terminal states
        self.rewards = np.full((self.size, self.size), -1.0)
        self.rewards[0, 0] = r  # Upper-left terminal state (reward 'r')
        self.rewards[0, 2] = 10  # Upper-right terminal state (reward 10)

    def value_iteration(self, theta=1e-3, max_iterations=1000, num_last_updates=5):
        values = np.zeros((self.size, self.size))  # Initializing all values to 0
        # Set the terminal state values explicitly
        values[0, 0] = self.rewards[0, 0]  # Upper-left terminal state
        values[0, 2] = self.rewards[0, 2]  # Upper-right terminal state

        # Store last `num_last_updates` iterations
        value_updates = []

        for iteration in range(max_iterations):
            delta = 0
            new_values = values.copy()

            for i in range(self.size):
                for j in range(self.size):
                    # Skip terminal states
                    if (i, j) == (0, 0) or (i, j) == (0, 2):
                        continue

                    # Calculate the value for all actions
                    action_values = []
                    for action in range(4):  # 0: Up, 1: Right, 2: Down, 3: Left
                        action_values.append(self.get_action_value(i, j, action, values))
                    
                    # Update the value of the state
                    new_values[i, j] = max(action_values)
                    delta = max(delta, abs(new_values[i, j] - values[i, j]))

            values = new_values
            value_updates.append(values.copy())

            if len(value_updates) > num_last_updates:
                value_updates.pop(0)

            if delta < theta:
                break

        # Print the last few value updates
        print(f"\nValue Function After Last {num_last_updates} Iterations:")
        for idx, update in enumerate(value_updates):
            print(f"Iteration {iteration - num_last_updates + idx + 1}:")
            print(update)

        self.policy = self.extract_policy(values)
        return values

    def get_action_value(self, x, y, action, values):
        transitions = self.get_transitions(x, y, action)
        value = 0
        for prob, nx, ny in transitions:
            reward = self.rewards[nx, ny]
            value += prob * (reward + self.discount_factor * values[nx, ny])
        return value

    def get_transitions(self, x, y, action):
        directions = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]  # Up, Down, Right, Left
        transitions = []

        for idx, (nx, ny) in enumerate(directions):
            prob = 0.8 if idx == action else 0.1  # 80% intended, 10% perpendicular
            if 0 <= nx < self.size and 0 <= ny < self.size:
                transitions.append((prob, nx, ny))
            else:
                transitions.append((prob, x, y))  # Collision with wall

        return transitions

    def extract_policy(self, values):
        policy = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                # Skip terminal states
                if (i, j) == (0, 0) or (i, j) == (0, 2):
                    continue
                action_values = [self.get_action_value(i, j, a, values) for a in range(4)]
                policy[i, j] = np.argmax(action_values)
        return policy

    def display_policy(self):
        symbols = {0: "↑", 1: "→", 2: "↓", 3: "←"}
        print("\nOptimal Policy:")
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == (0, 0):
                    print("UL", end="\t")  # Upper-left terminal
                elif (i, j) == (0, 2):
                    print("UR", end="\t")  # Upper-right terminal
                else:
                    print(symbols[self.policy[i, j]], end="\t")
            print()

if __name__ == "__main__":
    r_values = [100, 3, 0, -3]
    for r in r_values:
        print(f"\n=== Results for r = {r} ===")
        solver = GridWorldSolver(r)
        values = solver.value_iteration()
        print("\nFinal Value Function:")
        print(values)
        solver.display_policy()
