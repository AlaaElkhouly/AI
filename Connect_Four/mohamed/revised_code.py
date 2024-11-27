
import math

class ConnectFour:
    def __init__(self, max_depth=5):
        self.player1_board = 0  # bitboard for player 1
        self.player2_board = 0  # bitboard for player 2
        self.height = [0] * 7   # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth

    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]

    def drop_piece(self, player_bitboard, column):
        """Simulate dropping a piece in the given column."""
        mask = 1 << (column * 7 + self.height[column])
        player_bitboard |= mask
        self.height[column] += 1
        return player_bitboard

    def undo_drop_piece(self, player_bitboard, column):
        """Undo the last piece drop."""
        self.height[column] -= 1
        mask = 1 << (column * 7 + self.height[column])
        player_bitboard &= ~mask
        return player_bitboard

    def evaluate_board(self):
        """Evaluate the current board state for scoring."""
        directions = [1, 6, 7, 8]  # right, diagonal-left, vertical, diagonal-right
        score = 0

        for direction in directions:
            # Player 1 scoring
            player1_temp = self.player1_board & (self.player1_board >> direction)
            score += bin(player1_temp & (player1_temp >> (2 * direction))).count('1')

            # Player 2 scoring
            player2_temp = self.player2_board & (self.player2_board >> direction)
            score -= bin(player2_temp & (player2_temp >> (2 * direction))).count('1')

        return score

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

    def print_board(self):
        """Visualize the current board."""
        board = [[' ' for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * 7 + row)) & 1:
                    board[row][col] = 'X'
                elif (self.player2_board >> (col * 7 + row)) & 1:
                    board[row][col] = 'O'

        for row in reversed(board):
            print('|' + '|'.join(row) + '|')

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
        """Handle AI's move using Minimax."""
        print("AI is thinking...")
        _, move = self.minimax(self.max_depth, float('-inf'), float('inf'), False)
        print(f"AI chooses column {move}")
        self.player2_board = self.drop_piece(self.player2_board, move)

    def play_game(self):
        """Play the game."""
        while True:
            self.print_board()

            # Check for tie
            if len(self.get_valid_moves()) == 0:
                print("It's a tie!")
                break

            # Player's turn
            self.player_turn()

            # AI's turn
            self.computer_turn()


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=5)
    game.play_game()
