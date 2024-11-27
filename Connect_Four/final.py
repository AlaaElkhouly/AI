import random
import numpy as np
import pygame

class ConnectFour:
    def __init__(self, max_depth=5, heuristic_depth=3, use_alpha_beta=True):
        self.board = np.zeros((6, 7), int)  # 6x7 board initialized to 0
        self.max_depth = max_depth  # Maximum depth for the AI search
        self.heuristic_depth = heuristic_depth  # Depth for heuristic pruning
        self.use_alpha_beta = use_alpha_beta  # Flag for alpha-beta pruning
        self.current_player = 1  # Player 1 starts
        self.player1 = 'X'  # Representing Player 1 with 1
        self.player2 = 'O'  # Representing Player 2 (AI) with 2
        self.num_rows = 6
        self.num_cols = 7
        
        # BITBOARD
        self.player1_board = 0  # bitboard for player 1
        self.player2_board = 0  # bitboard for player 2
        self.height = [0] * 7   # column heights
        
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
        row = self.height[column]
        mask = 1 << (column * 7 + row)
        player_bitboard |= mask
        self.height[column] += 1
        return player_bitboard, row

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
            # Check control of the center column
            if (self.player1_board >> (center_column * 7 + row)) & 1:
                center_control_score += 1  # Player 1 controls the center
            elif (self.player2_board >> (center_column * 7 + row)) & 1:
                center_control_score -= 1  # Player 2 controls the center
        score += center_control_score * 3  # Giving more weight to the center

        # Helper function to count potential 2-in-a-row and 3-in-a-row for a given board
        def count_potential_wins(player_board):
            player_score = 0
            for direction in directions:
                temp_board = player_board & (player_board >> direction)
                # Count 3-in-a-row and 2-in-a-row
                player_score += bin(temp_board & (temp_board >> (2 * direction))).count('1')
                player_score += bin(temp_board & (temp_board >> direction)).count('1')  # 2-in-a-row
            return player_score

        # Count potential 2-in-a-row and 3-in-a-row for both players
        player1_score = count_potential_wins(self.player1_board)
        player2_score = count_potential_wins(self.player2_board)

        # Add the positive/negative scores for potential wins
        score += player1_score * 10  # Player 1 gets positive score
        score -= player2_score * 10  # Player 2 gets negative score (to discourage opponent's win)

        # Block opponent's potential winning moves
        def block_opponent(player_board, opponent_board):
            block_score = 0
            for direction in directions:
                opponent_temp_board = opponent_board & (opponent_board >> direction)
                block_score += bin(opponent_temp_board & (opponent_temp_board >> (2 * direction))).count('1')
            return block_score

        # Block player 1's and player 2's winning moves
        score -= block_opponent(self.player1_board, self.player2_board) * 50  # Block opponent's win
        score += block_opponent(self.player2_board, self.player1_board) * 50  # Block player 1 from winning

        return score

    def bitboard_to_2d_array(self):
        """Convert the bitboard to a 2D array representation."""
        board = [[' ' for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        # Convert player 1 bitboard to 'X' and player 2 bitboard to 'O'
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * 7 + row)) & 1:
                    board[row][col] = 'X'  # Player 1 piece
                elif (self.player2_board >> (col * 7 + row)) & 1:
                    board[row][col] = 'O'  # Player 2 piece

        return board

    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with optional alpha-beta pruning."""
        valid_moves = self.get_valid_moves()

        if depth == 0 or not valid_moves:
            return self.evaluate_board(), None

        best_move = None

        if maximizing_player:  # AI (Player 2)
            max_eval = float('-inf')
            for col in valid_moves:
                # Simulate the AI move
                player_bitboard, _ = self.drop_piece(self.player2_board, col)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.player2_board = self.undo_drop_piece(player_bitboard, col)  # Undo the move

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

                if self.use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

            return max_eval, best_move
        else:  # Human (Player 1)
            min_eval = float('inf')
            for col in valid_moves:
                # Simulate the human move
                player_bitboard, _ = self.drop_piece(self.player1_board, col)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.player1_board = self.undo_drop_piece(player_bitboard, col)  # Undo the move

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col

                if self.use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

            return min_eval, best_move

    def draw_board(self):
        """Draw the game board using Pygame."""
        self.screen.fill((0, 0, 0))

        # Draw the grid
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                pygame.draw.rect(self.screen, (0, 0, 255), (col * 100, row * 100, 100, 100))
                pygame.draw.circle(self.screen, (0, 255, 0), (col * 100 + 50, row * 100 + 50), 45)

        # Draw pieces based on bitboards
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * 7 + row)) & 1:
                    pygame.draw.circle(self.screen, (255, 255, 0), (col * 100 + 50, row * 100 + 50), 45)
                elif (self.player2_board >> (col * 7 + row)) & 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (col * 100 + 50, row * 100 + 50), 45)

        pygame.display.update()
        
    def is_full(self):
        """Check if the board is full (no valid moves left)."""
        return all(self.height[col] == self.num_rows for col in range(self.num_cols))


    def play_game(self):
        """Simulate the game with the AI and human player."""
        while True:
            print("Current Board:")
            self.draw_board()

            if self.current_player == 1:  # Human's turn
                print("Your Turn!")
                valid_moves = self.get_valid_moves()

                # Check for mouse click on columns
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        col = x // 100  # Divide the x-coordinate by 100 to get the column
                        if col in valid_moves:
                            self.player1_board, _ = self.drop_piece(self.player1_board, col)
                            self.current_player = 2
            else:  # AI's turn
                print("AI's Turn!")
                _, best_move = self.minimax(self.max_depth, float('-inf'), float('inf'), True)
                if best_move is not None:
                    self.player2_board, _ = self.drop_piece(self.player2_board, best_move)
                    self.current_player = 1

            if self.is_full():
                print("Game Over!")
                break
if __name__ == "__main__":
    game = ConnectFour(max_depth=5, use_alpha_beta=True)
    game.play_game()