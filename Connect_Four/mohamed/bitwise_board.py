class Board:
    def __init__(self):
        # Initialize bitboards for both players
        self.player1 = 0
        self.player2 = 0
        
        # Track the height of each column (number of pieces in each column)
        self.height = [0] * 7  # 7 columns in Connect Four

    def drop_piece(self, player, column):
        """Drop a piece for the given player in the specified column."""
        # Check if the column is full
        if self.height[column] >= 6:  # Max height is 6 rows
            raise ValueError(f"Column {column} is full.")
        
        # Calculate the mask for the position to drop the piece
        mask = 1 << (column * 7 + self.height[column])
        
        # Update the player's bitboard
        if player == 1:
            self.player1 |= mask
        else:
            self.player2 |= mask
        
        # Increment the height of the column
        self.height[column] += 1

    def __str__(self):
        """Visualize the board as a string (optional for debugging)."""
        board_repr = [["." for _ in range(7)] for _ in range(6)]
        for col in range(7):
            for row in range(6):
                pos = col * 7 + row
                if (self.player1 & (1 << pos)) != 0:
                    board_repr[row][col] = "X"
                elif (self.player2 & (1 << pos)) != 0:
                    board_repr[row][col] = "O"
        
        # Print from top to bottom (row-major order)
        return "\n".join([" ".join(row) for row in reversed(board_repr)])
