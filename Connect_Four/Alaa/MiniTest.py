#---------------------------------------------------------------------------------Alaa's Zone---------------------------------------------------------------------------------#
import random
import math
from anytree import Node
    def get_probabilities(self,column):
        if column == 0:
            return {0: 0.6, 1: 0.4}
        elif column == 6:
            return {6: 0.6, 5: 0.4}
        else:
            return {column - 1: 0.2, column: 0.6, column + 1: 0.2}
        
    def expecticol(self, column):
        probabilities=self.get_probabilities(column)
        rand = random.random()
        cumulative_probability = 0
        for key, probability in probabilities.items():
            cumulative_probability += probability
            if rand < cumulative_probability:
                ecol = key
        return ecol

    def player_turn_expecti(self):
            """Handle player's move."""
            while True:
                try:
                    move = self.expecticol(int(input("Your move (0-6): ")))
                    if move not in self.get_valid_moves():
                        print("Invalid move. Try again.")
                    else:
                        break
                except ValueError:
                    print("Please enter a number between 0 and 6.")
            self.player2_board = self.drop_piece(self.player2_board, move)

    def computer_turn_expecti(self):
        print("AI is thinking...")
        self.tree_root = Node("Root")  # Reset the tree for this turn
        _, move = self.expectiminimax(self.max_depth, True, self.tree_root)
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.display_tree() # Display the tree after the AI move
        print(f"AI chooses column {move}")

    def expectiminimax(self, depth, maximizing_player, parent_node=None):
        """Expected minimax to handle probabilistic moves and misplacement."""
        if depth == 0 or not self.get_valid_moves():
            score = self.evaluate_board()
            Node(f"score: {score}", parent=parent_node)
            return score, None

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            max_value = -math.inf
            for column in valid_moves:
                expected_value = 0

                # Get possible outcome columns and their probabilities
                probabilities = self.get_probabilities(column)

                # Choose one of the columns based on the probability distribution
                outcome_col = self.expecticol(column)
                # Ensure the chosen column isn't full
                if self.height[outcome_col] >= self.num_rows:  # Skip full columns
                    continue

                # Drop the piece in the chosen column based on misplacement probability
                self.player1_board = self.drop_piece(self.player1_board, outcome_col)

                # Create child node
                child_node = Node(f"(ai max) Move to column: {column} ,board: {board_string} ", parent=parent_node)

                value, _ = self.expectiminimax(depth - 1, False)
                self.player1_board = self.undo_drop_piece(self.player1_board, outcome_col)
                expected_value += probabilities[outcome_col] * value

                if expected_value > max_value:
                    max_value = expected_value
                    best_move = outcome_col

            return max_value, best_move
        else:
            min_value = math.inf
            for column in valid_moves:
                expected_value = 0

                # Get possible outcome columns and their probabilities
                probabilities = self.get_probabilities(column)

                # Choose one of the columns based on the probability distribution
                outcome_col =  self.expecticol(column)

                # Ensure the chosen column isn't full
                if self.height[outcome_col] >= self.num_rows:  # Skip full columns
                    continue

                # Drop the piece in the chosen column based on misplacement probability
                self.player2_board = self.drop_piece(self.player2_board, outcome_col)
                board_string= self.generate_board_string()

                # Create child node
                child_node = Node(f"(player min)Move: {column}, board: {board_string} ", parent=parent_node)

                value, _ = self.expectiminimax(depth - 1, True, child_node)
                self.player2_board = self.undo_drop_piece(self.player2_board, outcome_col)
                expected_value += probabilities[outcome_col] * value

                if expected_value < min_value:
                    min_value = expected_value
                    best_move = outcome_col

            return min_value, best_move