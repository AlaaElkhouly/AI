class ConnectFour:
    def __init__(self):
        self.player1 = 0  # Bitboard for Player 1
        self.player2 = 0  # Bitboard for Player 2
        self.height = [0] * 7  # Heights of columns
        self.num_rows = 6  # Number of rows
        self.num_cols = 7  # Number of columns
        self.queue=[]

    
    def get_valid_moves(self):
        """
        Get a list of valid columns where a piece can be dropped.
        :return: List of column indices that are not full.
        """
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows] #still is not full

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
        Count the number of connect fours for the given board.
        :param board: The bitboard of the current player.
        :return: The total number of connect fours (groups of four in a row).
        """
         directions = [1, 7, 6, 8]  # Offsets for horizontal, vertical, diagonal1, diagonal2
         player1_score=0
         player2_score=0# Initialize the count of connect fours
        

         for direction in directions:
            # Find pairs of connected pieces in the current direction
            player1_board = self.player1 & (self.player1 >> direction)
            # Find groups of four connected pieces and count them
            player1_score += bin(player1_score & (player1_score >> 2 * direction)).count('1')
            
            # Find pairs of connected pieces in the current direction
            player2_board = self.player2 & (self.player2 >> direction)
            # Find groups of four connected pieces and count them
            player2_score += bin(player2_score & (player2_score >> 2 * direction)).count('1')


         return player1_score,player1_score
     
    def simulate_moves(self, max_depth):
        """
        Simulate all possible moves up to a given depth and keep track of the states.
        :param max_depth: Maximum depth to simulate.
        """
        from copy import deepcopy

        self.queue.append((deepcopy(self.player1), deepcopy(self.player2)))  # Initial state

        for depth in range(max_depth):
            next_states = []
            for state in self.queue:
                player1, player2 = state
                for move in self.get_valid_moves():
                    new_player1 = self.drop_piece(player1, move, deepcopy(self.player1))
                    new_player2 = self.drop_piece(player2, move, deepcopy(self.player2))
                    next_states.append((new_player1, new_player2))

            self.queue.extend(next_states)

    def print_tree(self):
        """
        Print the tree of states stored in the queue.
        """
        for i, state in enumerate(self.queue):
            player1, player2 = state
            print(f"State {i}: Player 1 Bitboard: {bin(player1)} | Player 2 Bitboard: {bin(player2)}")




# Example usage
game = ConnectFour()
game.simulate_moves(max_depth=2)
game.print_tree()



def minimax(game, max_depth, alpha, beta, maximizing_player):

    """
    Minimax algorithm with alpha-beta pruning.
    :param game: The current ConnectFour game instance.
    :param depth: Current depth of the tree.
    :param alpha: Alpha value for pruning.
    :param beta: Beta value for pruning.
    :param maximizing_player: True if the current player is maximizing.
    :return: Best score and best move (column index).
    """
    max_depth=input("enter maximum depth")
    # Base case: Check for a terminal state or max depth
    if depth == max_depth:
       
        
        return game.evaluate_board(), None  # Heuristic score

    valid_moves = game.get_valid_moves() #get valid moves

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
