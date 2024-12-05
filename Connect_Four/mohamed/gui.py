from rebuild import *
import pygame
import sys

class GUI(ConnectFour):
    def __init__(self, max_depth=4):
        
        pygame.init()
        pygame.display.set_caption("Connect Four")
        super().__init__(max_depth)
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
        self.minimax_mode = 0 
        # Asking user for maximum depth and k using a text input box

        # Asking user for maximum depth and k using console input
        #self.max_depth = self.get_console_input("Enter the maximum depth (e.g., 4):")
        #self.k = self.get_console_input("Enter the truncation (k) value (e.g., 3):")

        # Game state
        self.board = self.get_corrected_board()
        self.current_player = 2  # Player starts as 2
        self.running = True
        
##-----------------------------------------------------get parameters-------------------------------------------##
    def get_console_input(self, prompt):
        """Ask for user input via the console."""
        while True:
            try:
                user_input = input(prompt)
                return int(user_input)  # Convert input to an integer
            except ValueError:
                print("Invalid input. Please enter an integer.")
                
##-----------------------------------------------------board operations--------------------------------------------##               
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
                
##-----------------------------------------------------toggle ai  mode--------------------------------------------##
    def toggle_minimax_mode(self):
        self.minimax_mode = (self.minimax_mode + 1) % 3  # Toggle between 0, 1, and 2
        
        
                      
    def draw_minimax_toggle(self):
            """Draw the minimax toggle button."""
            x, y, width, height = self.SCREEN_WIDTH - 140, 10, 140, 40  # Positioned at the far right
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, height), border_radius=10)
            label = self.small_font.render(f"{['Without α-β', 'With α-β', 'Expected'][self.minimax_mode]}", True, (0, 0, 0))
            self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

            # Draw Minimax text
            text_label = self.font.render("Minimax:", True, (0, 0, 0))
            self.screen.blit(text_label, (x - 100, y + 10))
            
##-----------------------------------------------------player mode--------------------------------------------##
    def handle_click(self, pos):
        """Handle player's move."""
        col = pos[0] // self.CELL_SIZE
        if col in self.get_valid_moves():
            self.player2_board = self.drop_piece(self.player2_board, col)
            if self.minimax_mode==0:
                self.current_player = 1     ##regular minimax
                
            elif self.minimax_mode==1:
                self.current_player = 3     ##alpha-beta
                
            elif self.minimax_mode==2:
                self.current_player = 4       ##expected
            self.update_game_state()
##-----------------------------------------------------different ai  modes--------------------------------------------##
    def ai_turn_regular_minimax(self):
        """AI's move."""
        print("AI is thinking...")
        self.tree_root = Node("Root")  # Reset the tree for this turn
        _, move = self.minimax(self.max_depth, True, self.tree_root)
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.display_tree() # Display the tree after the AI move
        ai_connect_4,player_connect_4=self.calculate_utility() 
        print(f"ai score is : {self.evaluate_board()}")                     
        print(f"AI chooses column {move}\n ai connected {ai_connect_4}, player connected{player_connect_4}")
        self.current_player = 2
        self.update_game_state()
        
    def ai_turn_alphabeta_minimax(self):
        """AI's move."""
        print("AI is thinking...")
        self.tree_root = Node("Root")  # Reset the tree for this turn
        _, move = self.minimax_with_alphabeta(self.max_depth, float('-inf'), float('inf'), True, self.tree_root)
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.display_tree() # Display the tree after the AI move
        ai_connect_4,player_connect_4=self.calculate_utility()
        print(f"ai score is : {self.evaluate_board()}")                      
        print(f"AI chooses column {move}\n ai connected {ai_connect_4}, player connected {player_connect_4}")
        self.current_player = 2
        self.update_game_state()
        
    def ai_turn_expected_minimax(self):
        """AI's move."""
        print("AI is thinking...")
        self.tree_root = Node("Root")  # Reset the tree for this turn
        _, move = self.expectiminimax(self.max_depth, True, self.tree_root)
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.display_tree() # Display the tree after the AI move
        ai_connect_4,player_connect_4=self.calculate_utility()
        print(f"ai score is : {self.evaluate_board()}")                      
        print(f"AI chooses column {move}\n ai connected {ai_connect_4}, player connected {player_connect_4}")
        self.current_player = 2
        self.update_game_state()
##----------------------------------------------game loop------------------------------------------------------##
    def update_game_state(self):
        """Update the game state and check for a winner."""
        self.board = self.get_corrected_board()  # Update the board using the overridden method
        self.draw_board()

    def game_loop(self):
        """Main game loop."""
        while self.running:
            self.draw_board()
            self.draw_minimax_toggle() 
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle the minimax toggle button click separately
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Check if the mouse click is within the Minimax toggle button
                    if self.SCREEN_WIDTH - 140 <= x <= self.SCREEN_WIDTH - 140 + 140 and 10 <= y <= 10 + 40:
                        self.toggle_minimax_mode()  # Toggle the mode when clicked
                    elif self.current_player == 2:
                        # Only handle the player's move if not clicking the toggle button
                        self.handle_click(event.pos)

            if self.current_player == 1:
                self.ai_turn_regular_minimax()
            elif self.current_player == 3: # 3 for alpha-beta
                self.ai_turn_alphabeta_minimax()
            elif self.current_player == 4:    # 4 for expectiminmax
                self.ai_turn_expected_minimax()


# Run the game
if __name__ == "__main__":
    game = GUI(max_depth=7)
    game.game_loop()
