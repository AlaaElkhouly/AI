import math

class ConnectFour:
    def __init__(self, max_depth=4):
        self.player1_board = 0b0  # bitboard for player 1
        self.player2_board = 0b0  # bitboard for player 2
        self.height = [0] * 7  # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.queue = []  # stores nodes for tree visualization
        self.scores = [0, 0]  # scores for player 1 and player 2
        self.k = 4

    # Get all valid moves
    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]

    # Tree operations
    def save_and_encode_tree(self):
        connect_four_board = ["."] * 42  # Use a list for the board visualization
        valid_moves = self.get_valid_moves()

        for column in valid_moves:
            copy_board1 = self.player1_board
            copy_board2 = self.player2_board

            temp_board2 = self.drop_piece(copy_board2, column)

            for i in range(42):
                if copy_board1 & (1 << i):
                    connect_four_board[i] = 'X'
                elif temp_board2 & (1 << i):
                    connect_four_board[i] = 'O'
                else:
                    connect_four_board[i] = '.'

            self.queue.append("".join(connect_four_board))
            self.undo_drop_piece(copy_board2, column)

    def decode_and_print_tree(self):
        """Decode and display all boards stored in the queue."""
        for node_index, c4_board in enumerate(self.queue):
            print(f"Node {node_index}:")
            print(c4_board)
            print()

    def clear_queue(self):
        self.queue.clear()

    # Drop and undo piece
    def drop_piece(self, player_bitboard, column):
        """Simulate dropping a piece in the given column."""
        if self.height[column] >= self.num_rows:
            raise ValueError("Column is full!")
        mask = 1 << (column * self.num_rows + self.height[column])
        player_bitboard |= mask
        self.height[column] += 1
        return player_bitboard

    def undo_drop_piece(self, player_bitboard, column):
        """Undo the last piece drop."""
        self.height[column] -= 1
        mask = 1 << (column * self.num_rows + self.height[column])
        player_bitboard &= ~mask
        return player_bitboard

    # Heuristic evaluation function
    def evaluate_board(self):
        """Evaluate the board state to calculate scores."""
        directions = [1, 7, 8, 6]
        player1_score = 0
        player2_score = 0

        for direction in directions:
            for shift in range(1, 4):
                player1_temp = self.player1_board & (self.player1_board >> direction)
                player2_temp = self.player2_board & (self.player2_board >> direction)
                player1_score += bin(player1_temp & (player1_temp >> (shift * direction))).count('1') * shift
                player2_score += bin(player2_temp & (player2_temp >> (shift * direction))).count('1') * shift

        self.scores = [player1_score, player2_score]
        return player1_score - player2_score

    # Minimax with alpha-beta pruning
    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax with alpha-beta pruning."""
        if depth == 0 or not self.get_valid_moves():
            return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            max_value = -math.inf
            for column in valid_moves:
                self.player1_board = self.drop_piece(self.player1_board, column)
                value, _ = self.minimax(depth - 1, alpha, beta, False)
                self.player1_board = self.undo_drop_piece(self.player1_board, column)

                if value > max_value:
                    max_value = value
                    best_move = column

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return max_value, best_move
        else:
            min_value = math.inf
            for column in valid_moves:
                self.player2_board = self.drop_piece(self.player2_board, column)
                value, _ = self.minimax(depth - 1, alpha, beta, True)
                self.player2_board = self.undo_drop_piece(self.player2_board, column)

                if value < min_value:
                    min_value = value
                    best_move = column

                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_value, best_move

    # Probabilities for expected minimax
    def get_probabilities(self, column):
        """Return a dictionary of potential column outcomes and their probabilities."""
        if column == 0:
            return {0: 0.6, 1: 0.4}
        elif column == 6:
            return {6: 0.6, 5: 0.4}
        else:
            return {column - 1: 0.2, column: 0.6, column + 1: 0.2}

    # Expected minimax
    def expected_minimax(self, depth, maximizing_player):
        """Expected minimax to handle probabilistic moves."""
        if depth == 0 or not self.get_valid_moves():
            return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            max_value = -math.inf
            for column in valid_moves:
                expected_value = 0
                for outcome_col, probability in self.get_probabilities(column).items():
                    if self.height[outcome_col] >= self.num_rows:  # Skip full columns
                        continue
                    self.player1_board = self.drop_piece(self.player1_board, outcome_col)
                    value, _ = self.expected_minimax(depth - 1, False)
                    self.player1_board = self.undo_drop_piece(self.player1_board, outcome_col)
                    expected_value += probability * value

                if expected_value > max_value:
                    max_value = expected_value
                    best_move = column

            return max_value, best_move
        else:
            min_value = math.inf
            for column in valid_moves:
                expected_value = 0
                for outcome_col, probability in self.get_probabilities(column).items():
                    if self.height[outcome_col] >= self.num_rows:  # Skip full columns
                        continue
                    self.player2_board = self.drop_piece(self.player2_board, outcome_col)
                    value, _ = self.expected_minimax(depth - 1, True)
                    self.player2_board = self.undo_drop_piece(self.player2_board, outcome_col)
                    expected_value += probability * value

                if expected_value < min_value:
                    min_value = expected_value
                    best_move = column

            return min_value, best_move

    # Print board
    def print_board(self):
        """Visualize the current board."""
        print(" 0 1 2 3 4 5 6")  # Column numbers
        board = [[' ' for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 'X'
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 'O'
        for row in reversed(board):
            print('|' + '|'.join(row) + '|')

    # Player and AI turns
    def player_turn(self):
        """Handle player's move."""
        while True:
            try:
                move = int(input("Your move (0-6): "))
                if move not in self.get_valid_moves():
                    print("Invalid move. Try again.")
                else:
                    break
            except ValueError:
                print("Please enter a number between 0 and 6.")
        self.player1_board = self.drop_piece(self.player1_board, move)

    def computer_turn(self):
        """Handle AI's move using Expected Minimax."""
        print("AI is thinking...")
        _, move = self.expected_minimax(5, True)
        if move is not None:
            print(f"AI chooses column {move}")
            self.player2_board = self.drop_piece(self.player2_board, move)
        else:
            print("AI could not find a valid move.")

    # Play game
    def play_game(self):
        """Play the game."""
        while True:
            self.print_board()
            if not self.get_valid_moves():
                print("Game over!")
                break
            self.player_turn()
            self.computer_turn()

# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=4)
    game.play_game()
