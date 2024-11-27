import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
ROWS = 6
COLUMNS = 7
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 10

# Colors and themes
THEMES = {
    "Classic": {"bg": (0, 0, 139), "player1": (255, 0, 0), "player2": (255, 255, 0)},
    "Ocean": {"bg": (0, 105, 148), "player1": (255, 128, 0), "player2": (255, 255, 102)},
    "Forest": {"bg": (34, 139, 34), "player1": (255, 69, 0), "player2": (154, 205, 50)},
    "Gray": {"bg": (169, 169, 169), "player1": (255, 255, 255), "player2": (70, 70, 70)},
}

class ConnectFourGame:
    def __init__(self):
        # Initialize game state
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = 1
        self.minimax_mode = 0  # 0: Without α-β, 1: With α-β, 2: Expected
        self.heuristic_mode = 1  # 1 or 2

        self.dropdown_active = False
        self.current_theme = "Classic"
        self.BACKGROUND_COLOR = THEMES[self.current_theme]["bg"]
        self.PLAYER_ONE_COLOR = THEMES[self.current_theme]["player1"]
        self.PLAYER_TWO_COLOR = THEMES[self.current_theme]["player2"]
        self.EMPTY_COLOR = (30, 30, 30)

        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

    def reset_game(self):
        """Reset the game board."""
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = 1

    def draw_board(self, screen):
        """Draw the game board and pieces."""
        screen.fill((255, 255, 255))  # White background

        # Draw grid and pieces
        for row in range(ROWS):
            for col in range(COLUMNS):
                pygame.draw.rect(screen, self.BACKGROUND_COLOR,
                                 (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, (0, 0, 0),
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                                   RADIUS + 5)

                # Draw pieces
                if self.board[row][col] == 0:
                    color = self.EMPTY_COLOR
                elif self.board[row][col] == 1:
                    color = self.PLAYER_ONE_COLOR
                else:
                    color = self.PLAYER_TWO_COLOR
                pygame.draw.circle(screen, color,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                                   RADIUS)

    def handle_piece_placement(self, pos):
        """Handle placing a piece on the board."""
        col = pos[0] // CELL_SIZE
        if col >= COLUMNS:
            return
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player
                return

    def get_valid_moves(self):
        """Get a list of valid moves (columns where pieces can be dropped)."""
        valid_moves = []
        for col in range(COLUMNS):
            if self.board[0][col] == 0:  # Check if top row is empty in the column
                valid_moves.append(col)
        return valid_moves

    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        valid_moves = self.get_valid_moves()
        if depth == 0 or not valid_moves:
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                self.make_move(move, self.current_player)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                self.make_move(move, 3 - self.current_player)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self):
        """Evaluate the board using the heuristic function."""
        # Heuristic evaluation logic for board
        # This can be based on piece count, line patterns, etc.
        return 0  # Placeholder evaluation, should be implemented with your heuristic

    def make_move(self, col, player):
        """Make a move for a player (used for minimax simulation)."""
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                break

    def undo_move(self, col):
        """Undo the last move made (used for minimax simulation)."""
        for row in range(ROWS):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                break

    def apply_theme(self, theme_name):
        """Apply the selected theme."""
        self.current_theme = theme_name
        self.BACKGROUND_COLOR = THEMES[theme_name]["bg"]
        self.PLAYER_ONE_COLOR = THEMES[theme_name]["player1"]
        self.PLAYER_TWO_COLOR = THEMES[theme_name]["player2"]

    def draw_new_game_button(self, screen):
        """Draw the New Game button."""
        pygame.draw.rect(screen, (0, 200, 0), (10, 10, 140, 40), border_radius=10)
        label = self.font.render("New Game", True, (0, 0, 0))
        screen.blit(label, (20, 20))

    def draw_minimax_toggle(self, screen):
        """Draw the minimax toggle button."""
        x, y, width, height = SCREEN_WIDTH - 140, 10, 140, 40
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
        label = self.small_font.render(f"{['Without α-β', 'With α-β', 'Expected'][self.minimax_mode]}", True, (0, 0, 0))
        screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
        text_label = self.font.render("Minimax:", True, (0, 0, 0))
        screen.blit(text_label, (x - 100, y + 10))

    def draw_heuristic_toggle(self, screen):
        """Draw the heuristic toggle button."""
        x, y, width, height = SCREEN_WIDTH - 40, 60, 40, 40
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
        label = self.small_font.render(f"{self.heuristic_mode}", True, (0, 0, 0))
        screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
        text_label = self.font.render("Heuristic:", True, (0, 0, 0))
        screen.blit(text_label, (x - 110, y + 10))


# Main game loop
def main():
    game = ConnectFourGame()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
    pygame.display.set_caption("Connect Four")
    running = True

    while running:
        game.draw_board(screen)
        game.draw_new_game_button(screen)
        game.draw_minimax_toggle(screen)
        game.draw_heuristic_toggle(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check New Game button
                if 10 <= pos[0] <= 150 and 10 <= pos[1] <= 50:
                    game.reset_game()

                # Check minimax toggle
                if SCREEN_WIDTH - 140 <= pos[0] <= SCREEN_WIDTH and 10 <= pos[1] <= 50:
                    game.minimax_mode = (game.minimax_mode + 1) % 3

                # Check heuristic toggle
                if SCREEN_WIDTH - 40 <= pos[0] <= SCREEN_WIDTH and 60 <= pos[1] <= 100:
                    game.heuristic_mode = 3 - game.heuristic_mode

                # Handle piece placement
                if game.dropdown_active:
                    game.handle_piece_placement(pos)

        pygame.display.update()

if __name__ == "__main__":
    main()
