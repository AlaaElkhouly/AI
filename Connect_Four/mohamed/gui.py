from rebuild import ConnectFour
import pygame
import sys

class GUI(ConnectFour):
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

        # Game state
        self.board = self.get_corrected_board()
        self.current_player = 2  # Player starts as 2
        self.running = True

    def get_corrected_board(self):
        """Override to ensure the board rows are reversed for GUI compatibility."""
        board = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.column_heights[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[self.num_rows - 1 - row][col] = 2  # AI pieces
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[self.num_rows - 1 - row][col] = 1  # Player pieces
        return board

    def draw_board(self):
        """Draw the game board and pieces."""
        self.screen.fill((255, 255, 255))  # White background

        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                pygame.draw.rect(self.screen, (0, 0, 139),
                                 (col * self.CELL_SIZE, row * self.CELL_SIZE + self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
                pygame.draw.circle(self.screen, (0, 0, 0),
                                   (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS + 5)

                # Draw pieces
                if self.board[row][col] == 0:
                    color = (30, 30, 30)
                elif self.board[row][col] == 1:
                    color = (255, 0, 0)  # Player 2 (human)
                else:
                    color = (255, 255, 0)  # Player 1 (AI)
                pygame.draw.circle(self.screen, color,
                                   (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS)

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

    def update_game_state(self):
        """Update the game state and check for a winner."""
        self.board = self.get_corrected_board()  # Update the board using the overridden method
        if self.check_win(self.board, 1):
            print("AI wins!")
            self.running = False
        elif self.check_win(self.board, 2):
            print("You win!")
            self.running = False
        elif not self.get_valid_moves():
            print("It's a draw!")
            self.running = False

    def game_loop(self):
        """Main game loop."""
        while self.running:
            self.draw_board()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.current_player == 2 and event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.current_player == 1:
                self.ai_turn()

# Run the game
if __name__ == "__main__":
    game = GUI(max_depth=4)
    game.game_loop()
