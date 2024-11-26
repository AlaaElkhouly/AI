##connect four class
class ConnectFour:
    def __init__(self):
        self.player1 = 0  # Bitboard for Player 1
        self.player2 = 0  # Bitboard for Player 2
        self.height = [0] * 7  # Heights of columns
        self.num_rows = 6  # Number of rows
        self.num_cols = 7  # Number of columns
        self.queue = []  # Queue for tracking game states
        self.game_depth=0
        
    def get_depth(self):
        self.game_depth=input("enter the game depth")

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
        self.height[column] += 1  # Update the height of the column
        return player_bitboard

    def undo_drop_piece(self, board, column):
        """
        Undo the last piece drop in a column.
        :param board: The current board (bitboard for the player).
        :param column: Column index to undo the piece drop.
        """
        self.height[column] -= 1  # Decrease the height
        mask = 1 << (column * 7 + self.height[column])
        board &= ~mask
        return board

    def evaluate_board(self):
        """
        Evaluate the current board to calculate the score for both players.
        :return: Tuple (Player 1 score, Player 2 score)
        """
        directions = [1, 7, 6, 8]  # Horizontal, vertical, and diagonal offsets
        player1_score = 0
        player2_score = 0

        for direction in directions:
            # Player 1 score calculation
            player1_board = self.player1 & (self.player1 >> direction)
            player1_score += bin(player1_board & (player1_board >> (2 * direction))).count('1')
            
            # Player 2 score calculation
            player2_board = self.player2 & (self.player2 >> direction)
            player2_score += bin(player2_board & (player2_board >> (2 * direction))).count('1')

        return player1_score, player2_score

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
                    new_player1 = self.drop_piece(deepcopy(player1), move, deepcopy(self.player1))
                    new_player2 = self.drop_piece(deepcopy(player2), move, deepcopy(self.player2))
                    next_states.append((new_player1, new_player2))

            self.queue.extend(next_states)

    def print_tree(self):
        """
        Print the tree of states stored in the queue.
        """
        for i, state in enumerate(self.queue):
            player1, player2 = state
            print(f"State {i}: Player 1 Bitboard: {bin(player1)} | Player 2 Bitboard: {bin(player2)}")

    def minimax(self, depth, alpha, beta, maximizing_player, use_alpha_beta=True):
        """
        Minimax algorithm with optional alpha-beta pruning.
        :param depth: Current depth of the tree.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param maximizing_player: True if the current player is maximizing.
        :param use_alpha_beta: Flag to decide whether to use alpha-beta pruning or not.
        :return: Best score and best move (column index).
        """
        depth = self.get_depth()
        
        # Base case: Check for a terminal state or max depth
        if depth == 0 or not self.get_valid_moves():
            player1_score, player2_score = self.evaluate_board()
            return player1_score - player2_score, None

        valid_moves = self.get_valid_moves()

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for col in valid_moves:
                # Simulate the move
                self.player1 = self.drop_piece(self.player1, col, self.player1)
                eval, _ = self.minimax(depth - 1, alpha, beta, False, use_alpha_beta)

                # Undo the move
                self.player1 = self.undo_drop_piece(self.player1, col)

                # Update the best score
                if eval > max_eval:
                    max_eval = eval
                    best_move = col

                if use_alpha_beta:
                    # Apply alpha-beta pruning
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for col in valid_moves:
                # Simulate the move
                self.player2 = self.drop_piece(self.player2, col, self.player2)
                eval, _ = self.minimax(depth - 1, alpha, beta, True, use_alpha_beta)

                # Undo the move
                self.player2 = self.undo_drop_piece(self.player2, col)

                # Update the best score
                if eval < min_eval:
                    min_eval = eval
                    best_move = col

                if use_alpha_beta:
                    # Apply alpha-beta pruning
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            return min_eval, best_move