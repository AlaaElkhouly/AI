from rebuild import ConnectFour


"GUI Working Code"
"Please Copy it in an empty file to edit it"
"DO NOT EDIT HERE! (Please)"
import pygame
import sys

class gui(ConnectFour):

   
    def __init__(self, max_depth=4):
        super().__init__(max_depth)
        pygame.init()
        pygame.display.set_caption("Connect Four")

        # Screen dimensions and constants
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 600
        self.ROWS = 6
        self.COLUMNS = 7
        self.CELL_SIZE = 100
        self.RADIUS = self.CELL_SIZE // 2 - 10
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT + 100))
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
            # Game state
        self.board = [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.current_player = 2
        self.dropdown_active = False
        self.minimax_mode = 0  # 0: "Without α-β", 1: "With α-β", 2: "Expected"
        self.heuristic_mode = 1  # 1 or 2
            # Colors and themes
        self.THEMES = {
            "Classic": {"bg": (0, 0, 139), "player1": (255, 0, 0), "player2": (255, 255, 0)},
            "Ocean": {"bg": (0, 105, 148), "player1": (255, 128, 0), "player2": (255, 255, 102)},
            "Forest": {"bg": (34, 139, 34), "player1": (255, 69, 0), "player2": (154, 205, 50)},
            "Gray": {"bg": (169, 169, 169), "player1": (255, 255, 255), "player2": (70, 70, 70)},
        }

        self.current_theme = "Classic"
        self.BACKGROUND_COLOR = self.THEMES[self.current_theme]["bg"]
        self.PLAYER_ONE_COLOR = self.THEMES[self.current_theme]["player1"]
        self.PLAYER_TWO_COLOR = self.THEMES[self.current_theme]["player2"]
        self.EMPTY_COLOR = (30, 30, 30)
    
  
        

        
    
    def draw_board(self):
        """Draw the game board and pieces."""
        self.screen.fill((255, 255, 255))  # White background

        # Draw grid and pieces
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                                (col * self.CELL_SIZE, row * self.CELL_SIZE + self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
                pygame.draw.circle(self.screen, (0, 0, 0),
                                (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE + self.CELL_SIZE // 2),
                                self.RADIUS + 5)

                # Draw pieces
                if self.board[row][col] == 0:
                    color = self.EMPTY_COLOR
                elif self.board[row][col] == 1:
                    color = self.PLAYER_ONE_COLOR
                else:
                    color = self.PLAYER_TWO_COLOR
                pygame.draw.circle(self.screen, color,
                                (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE + self.CELL_SIZE // 2),
                                self.RADIUS)


    def reset_game(self):
        """Reset the game board."""
        global board, current_player
        board = [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        current_player = 1


    def draw_new_game_button(self):
        """Draw the New Game button."""
        pygame.draw.rect(self.screen, (0, 200, 0), (10, 10, 140, 40), border_radius=10)  # Wider button
        label = self.font.render("New Game", True, (0, 0, 0))
        self.screen.blit(label, (20, 20))


    def draw_theme_dropdown(self):
        """Draw the theme dropdown menu."""
        pygame.draw.rect(self.screen, (150, 150, 255), (10, 60, 120, 40), border_radius=10)  # Moved to the left below New Game
        label = self.font.render("Theme", True, (0, 0, 0))
        self.screen.blit(label, (30, 70))

        if self.dropdown_active:
            for i, theme_name in enumerate(self.THEMES.keys()):
                pygame.draw.rect(self.screen, (200, 200, 200), (10, 100 + i * 40, 120, 40), border_radius=10)
                theme_label = self.font.render(theme_name, True, (0, 0, 0))
                self.screen.blit(theme_label, (20, 110 + i * 40))


    def apply_theme(self,theme_name):
        """Apply the selected theme."""
        global current_theme, BACKGROUND_COLOR, PLAYER_ONE_COLOR, PLAYER_TWO_COLOR
        current_theme = theme_name
        BACKGROUND_COLOR = self.THEMES[theme_name]["bg"]
        PLAYER_ONE_COLOR = self.THEMES[theme_name]["player1"]
        PLAYER_TWO_COLOR = self.THEMES[theme_name]["player2"]


    def draw_minimax_toggle(self):
        """Draw the minimax toggle button."""
        x, y, width, height = self.SCREEN_WIDTH - 140, 10, 140, 40  # Positioned at the far right
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, height), border_radius=10)
        label = self.small_font.render(f"{['Without α-β', 'With α-β', 'Expected'][self.minimax_mode]}", True, (0, 0, 0))
        self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

        # Draw Minimax text
        text_label = self.font.render("Minimax:", True, (0, 0, 0))
        self.screen.blit(text_label, (x - 100, y + 10))


    def draw_heuristic_toggle(self):
        """Draw the heuristic toggle button."""
        x, y, width, height = self.SCREEN_WIDTH - 40, 60, 40, 40  # Positioned at the very right
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, height), border_radius=10)
        label = self.small_font.render(f"{self.heuristic_mode}", True, (0, 0, 0))
        self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

        # Draw Heuristic text
        text_label = self.font.render("Heuristic:", True, (0, 0, 0))
        self.screen.blit(text_label, (x - 110, y + 10))


    def handle_piece_placement(self,pos):
        """Handle placing a piece on the board."""
        col = pos[0] // self.CELL_SIZE
        if col >= self.COLUMNS:
            return
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player
                return
            
    def handle_click(self, pos):
        """Handle player's move."""
        col = pos[0] // self.CELL_SIZE
        if col in self.get_valid_moves():
            self.player2_board = self.drop_piece(self.player2_board, col)
            self.current_player = 1
            self.update_game_state()
            
    def ai_turn(self):
        """AI's move."""
        print("AI is thinking...")
        _, move = self.minimax_with_alphabeta(self.max_depth, float('-inf'), float('inf'), True)
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.current_player = 2
        self.update_game_state()


    def is_board_full(self):
        """Check if the board is full (no empty spaces)."""
        for row in board:
            if 0 in row:
                return False
        return True
    
    def update_game_state(self):
        """Update the game state and check for a winner."""
        self.board = self.bitboard_to_array()

    def update_game(self):
            
        # Main game loop
        running = True
        while running:
            self.draw_board()
            self.draw_new_game_button()
            self.draw_theme_dropdown()
            self.draw_minimax_toggle()
            self.draw_heuristic_toggle()

            # Check Minimax and Heuristic modes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Check New Game button
                    if 10 <= pos[0] <= 150 and 10 <= pos[1] <= 50:
                        self.reset_game()

                    # Check theme dropdown
                    elif 10 <= pos[0] <= 130 and 60 <= pos[1] <= 100:  # Adjusted for left-side position
                        self.dropdown_active = not self.dropdown_active
                    elif self.dropdown_active and 10 <= pos[0] <= 130:
                        for i, theme_name in enumerate(self.THEMES.keys()):
                            if 100 + i * 40 <= pos[1] < 140 + i * 40:
                                self.apply_theme(theme_name)
                                self.dropdown_active = False

                    # Check minimax toggle
                    elif self.SCREEN_WIDTH - 140 <= pos[0] <= self.SCREEN_WIDTH and 10 <= pos[1] <= 50:
                        self.minimax_mode = (self.minimax_mode + 1) % 3

                    # Check heuristic toggle
                    elif self.SCREEN_WIDTH - 40 <= pos[0] <= self.SCREEN_WIDTH and 60 <= pos[1] <= 100:
                        self.heuristic_mode = 1 if self.heuristic_mode == 2 else 2

                    # Handle piece placement
                    elif pos[1] > self.CELL_SIZE:
                        self.handle_piece_placement(pos)

            pygame.display.update()
            print(self.board)
    
    def run_game(self):
        pass

    

# Run the game
if __name__ == "__main__":
    game=gui()
    game.update_game()