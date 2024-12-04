#---------------------------------------------------------------------------------Alaa's Zone---------------------------------------------------------------------------------#

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

    def expectiminimax(self, depth, maximizing_player, parent_node=None, current_level=1):
        """Expected minimax to handle probabilistic moves and misplacement."""
        if depth == 0 or not self.get_valid_moves():
            score = self.evaluate_board()
            if self.k is None or current_level <= self.k:
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
                
                # Drop the piece in the chosen column based on misplacement probability
                self.player1_board = self.drop_piece(self.player1_board, outcome_col)

                board_string = self.generate_board_string()

                # Create a child node only if within the first k levels
                child_node = None
                if self.k is None or current_level < self.k:
                    child_node = Node(f"(Max) Move: {column}, board: {board_string}", parent=parent_node)

                value, _ = self.expectiminimax(depth - 1, False ,child_node, current_level + 1)
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

                # Drop the piece in the chosen column based on misplacement probability
                self.player2_board = self.drop_piece(self.player2_board, outcome_col)
                board_string= self.generate_board_string()

                # Create a child node only if within the first k levels
                child_node = None
                if self.k is None or current_level < self.k:
                    child_node = Node(f"(Min) Move: {column}, board: {board_string}", parent=parent_node)

                value, _ = self.expectiminimax(depth - 1, True, child_node, current_level + 1)
                self.player2_board = self.undo_drop_piece(self.player2_board, outcome_col)
                expected_value += probabilities[outcome_col] * value

                if expected_value < min_value:
                    min_value = expected_value
                    best_move = outcome_col

            return min_value, best_move
        
    def play_game_expecti(self):
    #Play the game.'''
        while True:
            self.print_board_for_player()
            print(f"ai score is : {self.evaluate_board()}")
            if not self.get_valid_moves():
                print("Game over!")
                break
            # Player's turn
            self.player_turn_expecti()
            # AI's turn
            self.computer_turn_expecti()