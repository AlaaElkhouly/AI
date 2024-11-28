import pygame
import math
import sys

class ConnectFour:
    def __init__(self, rows=6, cols=7, square_size=100, max_depth=5, k=4):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.radius = square_size // 2 - 5
        self.player1_board = 0  # Bitboard for Player 1 (Human)
        self.player2_board = 0  # Bitboard for Player 2 (AI)
        self.height = [0] * cols  # Tracks the height of each column
        self.gui_initialized = False
        self.screen = None
        self.max_depth = max_depth
        self.k = k  # Max depth for heuristic truncation
        self.alpha_beta_enabled = True  # Default to alpha-beta pruning

    def initialize_gui(self):
        """Initialize the Pygame GUI."""
        pygame.init()
        width = self.cols * self.square_size
        height = (self.rows + 1) * self.square_size  # Extra row for the top
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Connect Four")
        self.gui_initialized = True

    def draw_board(self):
        """Draw the game board."""
        if not self.gui_initialized:
            self.initialize_gui()

        # Draw the empty grid
        for col in range(self.cols):
            for row in range(self.rows):
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 255),  # Blue for the board background
                    (col * self.square_size, (row + 1) * self.square_size, self.square_size, self.square_size),
                )
                pygame.draw.circle(
                    self.screen,
                    (0, 0, 0),  # Black for empty slots
                    (col * self.square_size + self.square_size // 2, (row + 1) * self.square_size + self.square_size // 2),
                    self.radius,
                )

        # Draw the pieces
        for col in range(self.cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * 7 + row)) & 1:
                    color = (255, 0, 0)  # Red for Player 1
                elif (self.player2_board >> (col * 7 + row)) & 1:
                    color = (255, 255, 0)  # Yellow for Player 2
                else:
                    continue
                pygame.draw.circle(
                    self.screen,
                    color,
                    (col * self.square_size + self.square_size // 2, (self.rows - row) * self.square_size + self.square_size // 2),
                    self.radius,
                )
        pygame.display.update()

    def get_valid_moves(self):
        """Return a list of valid columns for the next move."""
        return [col for col in range(self.cols) if self.height[col] < self.rows]

    def drop_piece(self, bitboard, column):
        """Simulate dropping a piece into the given column."""
        mask = 1 << (column * 7 + self.height[column])
        bitboard |= mask
        self.height[column] += 1
        return bitboard

    def undo_drop_piece(self, bitboard, column):
        """Undo the last piece drop in the given column."""
        self.height[column] -= 1
        mask = 1 << (column * 7 + self.height[column])
        bitboard &= ~mask
        return bitboard

    def evaluate_board(self):
        """Heuristic evaluation of the board state."""
        directions = [1, 7, 6, 8]
        score = 0

        for direction in directions:
            # Player 1 scoring
            player1_temp = self.player1_board & (self.player1_board >> direction)
            score += bin(player1_temp & (player1_temp >> (2 * direction))).count("1")

            # Player 2 scoring
            player2_temp = self.player2_board & (self.player2_board >> direction)
            score -= bin(player2_temp & (player2_temp >> (2 * direction))).count("1")

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

    def player_turn(self):
        """Handle the player's move."""
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
        """Handle the AI's move."""
        print("AI is thinking...")
        if self.alpha_beta_enabled:
            _, move = self.minimax(self.k, float("-inf"), float("inf"), False)
        else:
            _, move = self.minimax(self.k, float("-inf"), float("inf"), False)  # Without alpha-beta pruning
        print(f"AI chooses column {move}")
        self.player2_board = self.drop_piece(self.player2_board, move)

    def play_game(self):
        """Run the game loop."""
        while True:
            self.draw_board()

            # Check for tie
            if len(self.get_valid_moves()) == 0:
                print("It's a tie!")
                break

            # Player's turn
            self.player_turn()
            if self.check_winner(self.player1_board):
                self.draw_board()
                print("You win!")
                break

            # AI's turn
            self.computer_turn()
            if self.check_winner(self.player2_board):
                self.draw_board()
                print("AI wins!")
                break


# Run the game
if __name__ == "__main__":
    game = ConnectFour(rows=6, cols=7, square_size=100, max_depth=5, k=4)
    game.play_game()
