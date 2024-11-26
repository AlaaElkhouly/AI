import pygame
import sys
import random

# Define constants
WIDTH, HEIGHT = 700, 600  # Window size
ROW_COUNT, COLUMN_COUNT = 6, 7  # Grid size
SQUARESIZE = 100  # Size of each cell in the grid
RADIUS = int(SQUARESIZE / 2 - 5)  # Radius of each piece
MARGIN = 20  # Margin for the game info
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT_SIZE = 40  # Font size for messages

# Initialize pygame
pygame.init()

# Explicitly initialize the font module (in case it wasn't initialized automatically)
pygame.font.init()

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four Game")

# Load font for messages
FONT = pygame.font.SysFont("monospace", FONT_SIZE)  # Font for messages

class ConnectFour:
    def __init__(self):
        self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]  # Empty board
        self.height = [0] * COLUMN_COUNT  # Tracks height of each column
        self.turn = 1  # Player 1 starts (1 = Player 1, -1 = Player 2)
        self.game_over = False  # Flag to check if the game is over

    def draw_board(self):
        """Draw the game grid and the pieces."""
        screen.fill(BLUE)
        
        # Draw the empty grid (background)
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, WHITE, (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)

        # Draw the pieces for each player
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
                elif self.board[r][c] == -1:
                    pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)

        pygame.display.update()

    def drop_piece(self, col, player):
        """Drop a piece in the selected column."""
        for r in range(ROW_COUNT - 1, -1, -1):  # Start from the bottom row
            if self.board[r][col] == 0:
                self.board[r][col] = player
                self.height[col] += 1
                break

    def check_win(self):
        """Check if there is a winning line in the grid."""
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.board[r][c] != 0:
                    if self.check_direction(r, c, 1, 0) or \
                       self.check_direction(r, c, 0, 1) or \
                       self.check_direction(r, c, 1, 1) or \
                       self.check_direction(r, c, 1, -1):
                        return True
        return False

    def check_direction(self, r, c, dr, dc):
        """Check for 4 consecutive pieces in a direction (dr, dc)."""
        player = self.board[r][c]
        for i in range(1, 4):
            nr, nc = r + i * dr, c + i * dc
            if not (0 <= nr < ROW_COUNT and 0 <= nc < COLUMN_COUNT) or self.board[nr][nc] != player:
                return False
        return True

    def evaluate_board(self):
        """Evaluate the board and return a score based on the pieces."""
        # Count pieces for each player (could be refined with more heuristics)
        player1_score = sum(row.count(1) for row in self.board)
        player2_score = sum(row.count(-1) for row in self.board)
        return player1_score - player2_score  # Player 1 wants to maximize, Player 2 minimizes

    def get_valid_moves(self):
        """Return valid column indices where a piece can be dropped."""
        return [col for col in range(COLUMN_COUNT) if self.height[col] < ROW_COUNT]

    def minimax(self, depth, maximizing_player):
        """Minimax algorithm without pruning."""
        if depth == 0 or self.check_win():
            return self.evaluate_board(), None  # Return the evaluation score

        valid_moves = self.get_valid_moves()
        if maximizing_player:  # AI's turn
            max_eval = float('-inf')
            best_move = None
            for col in valid_moves:
                self.drop_piece(col, 1)  # AI plays (Player 1)
                eval, _ = self.minimax(depth - 1, False)
                self.undo_move(col)
                if eval > max_eval:
                    max_eval = eval
                    best_move = col
            return max_eval, best_move
        else:  # Human player's turn
            min_eval = float('inf')
            best_move = None
            for col in valid_moves:
                self.drop_piece(col, -1)  # Human plays (Player 2)
                eval, _ = self.minimax(depth - 1, True)
                self.undo_move(col)
                if eval < min_eval:
                    min_eval = eval
                    best_move = col
            return min_eval, best_move

    def undo_move(self, col):
        """Undo the last move by clearing the last dropped piece."""
        for r in range(ROW_COUNT):
            if self.board[r][col] != 0:
                self.board[r][col] = 0
                self.height[col] -= 1
                break

    def show_game_over(self, result):
        """Display the game over message."""
        message = FONT.render(f"{result} Wins!", True, WHITE)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, MARGIN))
        pygame.display.update()

    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
        self.height = [0] * COLUMN_COUNT
        self.turn = 1
        self.game_over = False
        self.draw_board()

# Initialize the game
game = ConnectFour()

# Main game loop
while True:
    game.draw_board()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            mouseX = event.pos[0]
            pygame.draw.circle(screen, RED if game.turn == 1 else YELLOW, (mouseX, SQUARESIZE // 2), RADIUS)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            col = mouseX // SQUARESIZE
            if game.height[col] < ROW_COUNT:
                game.drop_piece(col, 1)  # Human player (Player 1)

                # Check for win after human's move
                if game.check_win():
                    game.game_over = True
                    game.show_game_over("Player 1")
                    break

                # AI move (Player 2)
                _, ai_move = game.minimax(4, False)  # Max depth of 4 for AI
                game.drop_piece(ai_move, -1)

                # Check for win after AI's move
                if game.check_win():
                    game.game_over = True
                    game.show_game_over("Player 2")
                    break

    pygame.display.update()
