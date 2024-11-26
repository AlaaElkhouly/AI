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
