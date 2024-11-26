class ConnectFour:
    def __init__(self):
        self.player1 = 0  # Bitboard for Player 1
        self.player2 = 0  # Bitboard for Player 2
        self.height = [0] * 7  # Heights of columns
        self.num_rows = 6  # Number of rows
        self.num_cols = 7  # Number of columns

    def check_win(self, board):
        """
        Check if a player has won.
        :param board: The bitboard of the current player.
        :return: True if the player has four in a row.
        """
        directions = [1, 7, 6, 8]  # Horizontal, Vertical, Diagonal1, Diagonal2
        for direction in directions:
            bb = board & (board >> direction)
            if bb & (bb >> 2 * direction):
                return True
        return False

    def get_valid_moves(self):
        """
        Get a list of valid columns where a piece can be dropped.
        :return: List of column indices that are not full.
        """
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]

    def drop_piece(self, board, column, player_bitboard):
        """
        Simulate dropping a piece in the column for the player.
        :param board: The current board (bitboard for the player).
        :param column: Column index to drop the piece.
        :param player_bitboard: The player's bitboard.
        :return: Updated player bitboard.
        """
        mask = 1 << (column * 7 + self.height[column])
        player_bitboard |= mask
        return player_bitboard

    def evaluate_board(self):
        """
        Heuristic to evaluate the board.
        :return: Score for the current board state.
        """
        # A simple heuristic: number of connected pieces
        player1_score = bin(self.player1).count('1')
        player2_score = bin(self.player2).count('1')
        return player1_score - player2_score









def minimax(game, depth, alpha, beta, maximizing_player):

    """
    Minimax algorithm with alpha-beta pruning.
    :param game: The current ConnectFour game instance.
    :param depth: Current depth of the tree.
    :param alpha: Alpha value for pruning.
    :param beta: Beta value for pruning.
    :param maximizing_player: True if the current player is maximizing.
    :return: Best score and best move (column index).
    """
    # Base case: Check for a terminal state or max depth
    if depth == 0 or game.check_win(game.player1) or game.check_win(game.player2):
        if game.check_win(game.player1):
            return 1000, None  # Maximizing player wins
        elif game.check_win(game.player2):
            return -1000, None  # Minimizing player wins
        else:
            return game.evaluate_board(), None  # Heuristic score

    valid_moves = game.get_valid_moves()

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for col in valid_moves:
            # Simulate the move
            new_board = game.drop_piece(game.player1, col, game.player1)
            game.height[col] += 1

            # Recursively call minimax
            eval, _ = minimax(game, depth - 1, alpha, beta, False)

            # Undo the move
            game.player1 &= ~(1 << (col * 7 + game.height[col] - 1))
            game.height[col] -= 1

            # Update the best score
            if eval > max_eval:
                max_eval = eval
                best_move = col

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for col in valid_moves:
            # Simulate the move
            new_board = game.drop_piece(game.player2, col, game.player2)
            game.height[col] += 1

            # Recursively call minimax
            eval, _ = minimax(game, depth - 1, alpha, beta, True)

            # Undo the move
            game.player2 &= ~(1 << (col * 7 + game.height[col] - 1))
            game.height[col] -= 1

            # Update the best score
            if eval < min_eval:
                min_eval = eval
                best_move = col

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move




##trial example##
game = ConnectFour()

# Example: Simulate a few moves
game.player1 = 0
game.player2 = 0
game.height = [0] * 7

# Let the AI calculate the best move
depth = 4  # Search 4 moves ahead
score, best_move = minimax(game, depth, float('-inf'), float('inf'), True)
print(f"Best Move: {best_move}, Score: {score}")



def evaluate_board(self):
    """
    Evaluate the board using a more advanced heuristic.
    :return: A score representing the value of the board state for Player 1.
    """
    def score_window(window, player_bitboard, opponent_bitboard):
        """Evaluate a 4-slot window for a given player."""
        player_count = sum((1 << pos) & player_bitboard > 0 for pos in window)
        opponent_count = sum((1 << pos) & opponent_bitboard > 0 for pos in window)
        
        if player_count > 0 and opponent_count > 0:
            return 0  # Mixed window, no advantage to anyone
        elif player_count == 4:
            return 100  # Winning position
        elif player_count == 3:
            return 5  # Strong threat
        elif player_count == 2:
            return 2  # Weak threat
        elif opponent_count == 4:
            return -100  # Opponent winning
        elif opponent_count == 3:
            return -5  # Opponent strong threat
        elif opponent_count == 2:
            return -2  # Opponent weak threat
        return 0

    # Directions for checking 4-in-a-row
    directions = [
        (1, 2, 3, 4),     # Horizontal
        (7, 14, 21, 28),  # Vertical
        (6, 12, 18, 24),  # Diagonal /
        (8, 16, 24, 32)   # Diagonal \
    ]
    
    score = 0

    # Evaluate the board for all possible 4-in-a-row combinations
    for col in range(self.num_cols):
        for row in range(self.num_rows):
            start_pos = col * 7 + row  # Calculate the starting bit position
            for direction in directions:
                window = [start_pos + d for d in direction if start_pos + d < 64]
                if len(window) == 4:  # Only consider full 4-slot windows
                    score += score_window(window, self.player1, self.player2)

    # Bonus for central column control
    center_column = 3
    center_positions = [center_column * 7 + r for r in range(self.num_rows)]
    center_count_player1 = sum((1 << pos) & self.player1 > 0 for pos in center_positions)
    center_count_player2 = sum((1 << pos) & self.player2 > 0 for pos in center_positions)
    score += 3 * (center_count_player1 - center_count_player2)

    return score
