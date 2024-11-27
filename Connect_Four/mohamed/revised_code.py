import pygame
import math

class ConnectFour:
    def __init__(self, max_depth=5):
        self.player1_board = 0  # bitboard for player 1
        self.player2_board = 0  # bitboard for player 2
        self.height = [0] * 7   # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Connect Four")
        self.clock = pygame.time.Clock()

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
        """Enhanced evaluation of the board for better AI performance."""
        directions = [1, 6, 7, 8]  # right, vertical, diagonal-left, diagonal-right
        score = 0

        # Center control: Favor the center columns more
        center_column = 3  # 3 is the center column for a 7-column board
        center_control_score = 0
        for row in range(self.num_rows):
            if (self.player1_board >> (center_column * 7 + row)) & 1:
                center_control_score += 1  # Player 1 controls the center
            elif (self.player2_board >> (center_column * 7 + row)) & 1:
                center_control_score -= 1  # Player 2 controls the center
        score += center_control_score * 3  # Giving more weight to the center

        # Scoring based on 2-in-a-row, 3-in-a-row for both players
        def count_potential_wins(player_board):
            """Counts the potential 2-in-a-row and 3-in-a-row for a player."""
            player_score = 0
            for direction in directions:
                temp_board = player_board & (player_board >> direction)
                player_score += bin(temp_board & (temp_board >> (2 * direction))).count('1')
                player_score += bin(temp_board & (temp_board >> direction)).count('1')  # 2-in-a-row
            return player_score

        # Count potential 2-in-a-row and 3-in-a-row for both players
        player1_score = count_potential_wins(self.player1_board)
        player2_score = count_potential_wins(self.player2_board)

        # Add the positive/negative scores for potential wins
        score += player1_score * 10  # Player 1 gets positive score
        score -= player2_score * 10  # Player 2 gets negative score (to discourage opponent's win)

        # Blocking opponent's 3-in-a-row or potential win
        def block_opponent(player_board, opponent_board):
            """Block opponent's potential 3-in-a-row or winning position."""
            block_score = 0
            for direction in directions:
                opponent_temp_board = opponent_board & (opponent_board >> direction)
                block_score += bin(opponent_temp_board & (opponent_temp_board >> (2 * direction))).count('1')
            return block_score

        # Block opponent's potential winning moves
        block_score = block_opponent(self.player1_board, self.player2_board)
        score -= block_score * 50  # Blocking is very important

        block_score = block_opponent(self.player2_board, self.player1_board)
        score += block_score * 50  # Block player 1 from winning

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

        # Print in terminal
        print("Board:")
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

    def draw_board(self):
        """Draw the game board using Pygame."""
        self.screen.fill((0, 0, 0))

        # Draw the grid
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                pygame.draw.rect(self.screen, (0, 0, 255), (col * 100, row * 100, 100, 100))
                pygame.draw.circle(self.screen, (0, 255, 0), (col * 100 + 50, row * 100 + 50), 45)

        # Draw pieces
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * 7 + row)) & 1:
                    pygame.draw.circle(self.screen, (255, 255, 0), (col * 100 + 50, row * 100 + 50), 45)
                elif (self.player2_board >> (col * 7 + row)) & 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (col * 100 + 50, row * 100 + 50), 45)

        pygame.display.update()

    def play_game(self):
        """Play the game."""
        while True:
            self.draw_board()
            self.print_board()

            # Check for a winner or tie
            if len(self.get_valid_moves()) == 0:
                print("Game Over: Tie!")
                break

            # Player's turn
            self.player_turn()

            # AI's turn
            self.computer_turn()


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=5)
    game.play_game()
