import random
import numpy as np

class ConnectFour:
    def __init__(self, max_depth=5, heuristic_depth=3, use_alpha_beta=True):
        self.board = np.zeros((6, 7), int)  # 6x7 board initialized to 0
        self.max_depth = max_depth  # Maximum depth for the AI search
        self.heuristic_depth = heuristic_depth  # Depth for heuristic pruning
        self.use_alpha_beta = use_alpha_beta  # Flag for alpha-beta pruning
        self.current_player = 1  # Player 1 starts
        self.game_tree = []  # To store game tree states for tracing
        self.player1 = 1  # Representing Player 1 with 1
        self.player2 = 2  # Representing Player 2 (AI) with 2

    def get_valid_moves(self):
        """Returns a list of valid column indices (0-6) where a piece can be dropped."""
        return [col for col in range(7) if self.board[0][col] == 0]  # Column is open if top row is 0

    def drop_piece(self, col, player):
        """Simulate dropping a piece for the current player in the given column."""
        for row in range(5, -1, -1):  # Drop the piece from bottom to top
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return row, col
        return None

    def undo_drop_piece(self, row, col):
        """Undo the last move for a player."""
        self.board[row][col] = 0

    def evaluate_board(self):
        """Evaluate the board using a heuristic."""
        return self.heuristic()

    def heuristic(self):
        """Heuristic function to evaluate the board."""
        score = 0
        # Score based on how many 2-in-a-rows, 3-in-a-rows, and 4-in-a-rows exist for each player
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == self.player1:
                    score += self.score_position(row, col, self.player1)
                elif self.board[row][col] == self.player2:
                    score -= self.score_position(row, col, self.player2)
        return score

    def score_position(self, row, col, player):
        """Calculate a score for a given position on the board."""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal /
        for direction in directions:
            score += self.check_line(row, col, direction[0], direction[1], player)
        return score

    def check_line(self, row, col, d_row, d_col, player):
        """Check for alignments of the player's discs in the specified direction."""
        count = 0
        for i in range(4):  # Check for a line of 4
            r, c = row + d_row * i, col + d_col * i
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
        return count

    def minimax(self, depth, alpha, beta, maximizing_player, game_state=None):
        """Minimax algorithm with optional alpha-beta pruning."""
        valid_moves = self.get_valid_moves()

        if depth == 0 or not valid_moves:
            return self.evaluate_board(), None

        if maximizing_player:  # AI (Player 2)
            max_eval = float('-inf')
            best_move = None
            for col in valid_moves:
                row, _ = self.drop_piece(col, self.player2)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False, game_state)
                self.undo_drop_piece(row, col)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col
                if self.use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            if game_state is not None:
                game_state.append(self.board.copy())  # Save the state to the game tree
            return max_eval, best_move
        else:  # Human (Player 1)
            min_eval = float('inf')
            best_move = None
            for col in valid_moves:
                row, _ = self.drop_piece(col, self.player1)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True, game_state)
                self.undo_drop_piece(row, col)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col
                if self.use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            if game_state is not None:
                game_state.append(self.board.copy())  # Save the state to the game tree
            return min_eval, best_move

    def expected_minimax(self, depth, maximizing_player, game_state=None):
        """Expected Minimax with probabilities for moving to adjacent columns."""
        valid_moves = self.get_valid_moves()
        if depth == 0 or not valid_moves:
            return self.evaluate_board(), None

        if maximizing_player:  # AI (Player 2)
            max_eval = float('-inf')
            best_move = None
            for col in valid_moves:
                row, _ = self.drop_piece(col, self.player2)
                eval_score, _ = self.expected_minimax(depth - 1, False, game_state)
                self.undo_drop_piece(row, col)
                max_eval = max(max_eval, eval_score)
                best_move = col
            if game_state is not None:
                game_state.append(self.board.copy())  # Save the state to the game tree
            return max_eval, best_move
        else:  # Human (Player 1)
            min_eval = float('inf')
            best_move = None
            for col in valid_moves:
                row, _ = self.drop_piece(col, self.player1)
                eval_score, _ = self.expected_minimax(depth - 1, True, game_state)
                self.undo_drop_piece(row, col)
                min_eval = min(min_eval, eval_score)
                best_move = col
            if game_state is not None:
                game_state.append(self.board.copy())  # Save the state to the game tree
            return min_eval, best_move

    def print_game_tree(self, game_tree):
        """Recursively prints the game tree."""
        for level, state in enumerate(game_tree):
            print(f"Level {level}:")
            self.print_board(state)
            print("\n")

    def print_board(self, board):
        """Prints the board in a readable format."""
        for row in board:
            print(' '.join(map(str, row)))
        print("-" * 7)

    def play_game(self):
        """Simulate the game with the AI and human player."""
        while True:
            print("Current Board:")
            print(self.board)
            if self.current_player == 1:  # Human's turn
                print("Your Turn!")
                valid_moves = self.get_valid_moves()
                move = int(input(f"Choose a column (0-6): "))
                if move in valid_moves:
                    row, _ = self.drop_piece(move, self.player1)
                    self.current_player = 2  # Switch to AI
                else:
                    print("Invalid move. Try again.")
            else:  # AI's turn
                print("AI's Turn!")
                game_tree = []  # Initialize the game tree
                eval_score, best_move = self.minimax(self.max_depth, float('-inf'), float('inf'), True, game_tree)
                print(f"AI chooses column: {best_move}")
                row, _ = self.drop_piece(best_move, self.player2)
                self.current_player = 1  # Switch to human

                # Print the game tree
                print("Game Tree:")
                self.print_game_tree(game_tree)
                
            if not self.get_valid_moves():
                print("Game Over! It's a draw.")
                break

if __name__ == "__main__":
    game = ConnectFour(max_depth=5, heuristic_depth=3, use_alpha_beta=True)  # Set depth and alpha-beta pruning
    game.play_game()
