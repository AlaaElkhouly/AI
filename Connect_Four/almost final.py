import math
import numpy as np
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

class ConnectFour:
    def __init__(self, max_depth=4):
        self.player1_board = 0b0  # bitboard for player 1
        self.player2_board = 0b0  # bitboard for player 2
        self.height = [0] * 7  # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.queue = []  # stores nodes for tree visualization
        self.scores = [0, 0]  # scores for player 1 and player 2
        self.k = 5
        self.COLS = self.num_cols
        self.ROWS = self.num_rows

    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]

    def save_and_encode_tree(self):
        connect_four_board = ["."] * 42  # Use a list for the board visualization
        self.queue.clear()  # Clear previous queue

        valid_moves = self.get_valid_moves()

        for column in valid_moves:
            # Get the bitboard for Player 1 and Player 2
            copy_board1 = self.player1_board
            copy_board2 = self.player2_board

            # Temporarily drop a piece for Player 2
            temp_board2 = self.drop_piece(copy_board2, column)

            # Visualize the bitboard state
            for i in range(42):
                if copy_board1 & (1 << i):  # Check if the i-th bit is set for Player 1
                    connect_four_board[i] = 'X'
                elif temp_board2 & (1 << i):  # Check if the i-th bit is set for Player 2
                    connect_four_board[i] = 'O'
                else:
                    connect_four_board[i] = '.'  # Empty space

            # Add the visualized board to the queue
            self.queue.append("".join(connect_four_board))
            self.undo_drop_piece(copy_board2, column)

    def decode_and_print_tree(self):
        """Decode and display all boards stored in the queue."""
        for node_index, c4_board in enumerate(self.queue):
            print(f"Node {node_index}:")
            print(c4_board)
            print()

    def drop_piece(self, player_bitboard, column):
        """Simulate dropping a piece in the given column."""
        if self.height[column] >= self.num_rows:
            raise ValueError("Column is full!")
        mask = 1 << (column * self.num_rows + self.height[column])
        player_bitboard |= mask
        self.height[column] += 1
        return player_bitboard

    def undo_drop_piece(self, player_bitboard, column):
        """Undo the last piece drop."""
        self.height[column] -= 1
        mask = 1 << (column * self.num_rows + self.height[column])
        player_bitboard &= ~mask
        return player_bitboard

    def evaluate_board(self):
        player_score = self.heuristic(self.player1_board, PLAYER_PIECE)
        ai_score = self.heuristic(self.player2_board, AI_PIECE)
        self.scores = [player_score, ai_score]
        #print(f"Debug: Player score = {player_score}, AI score = {ai_score}")
        return ai_score - player_score

    def check_win(self, board, piece):
        ROWS = self.num_rows
        COLS = self.num_cols
        # Horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(board[row][col + i] == piece for i in range(4)):
                    return True
        # Vertical
        for row in range(ROWS - 3):
            for col in range(COLS):
                if all(board[row + i][col] == piece for i in range(4)):
                    return True
        # Diagonal (sloping downward from left to right)
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(board[row + i][col + i] == piece for i in range(4)):
                    return True
        # Diagonal (sloping downward from right to left)
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(board[row - i][col + i] == piece for i in range(4)):
                    return True

        return False

    def bitboard_to_array(self,bitboard, rows, cols):
        board = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 1
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 2
        print(board)
        return board

    def heuristic(self, bitboard, piece):
        ROWS = self.num_rows
        COLS = self.num_cols
        board=self.bitboard_to_array(bitboard,ROWS,COLS)
        #print(board)
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        # Feature 1: Absolute win
        if self.check_win(board, piece):
            return float('inf')  # AI wins
        if self.check_win(board, opp_piece):
            return float('-inf')  # Opponent wins

        # Horizontal scoring
        for row in range(ROWS):
            for col in range(COLS - 3):
                window = board[row][col:col + 4]
                score += self.evaluate_window_heuristic1(window, board, piece, row, col, direction='horizontal')

        # Vertical scoring
        for row in range(ROWS - 3):
            for col in range(COLS):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window_heuristic1(window, board, piece, row, col, direction='vertical')

        # Positive diagonal scoring
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window_heuristic1(window, board, piece, row, col, direction='positive_diagonal')

        # Negative diagonal scoring
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window_heuristic1(window, board, piece, row, col, direction='negative_diagonal')

        # Feature 4: Single chessmen position evaluation
        score += self.single_piece_heuristic(board, piece)
        #print(score)

        return score

    def evaluate_window_heuristic1(self, window, board, piece, row, col, direction):
        # Evaluate a window of 4 cells for Heuristic-1 features.
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        count_piece = np.count_nonzero(np.array(window) == piece)
        count_empty = np.count_nonzero(np.array(window) == EMPTY)
        count_opp_piece = np.count_nonzero(np.array(window) == opp_piece)

        # Feature 1: Absolute win
        if count_piece == 4:
            return float('inf')  # Absolute win

        # Feature 2: Three connected (3 situation)
        if count_piece == 3 and count_empty == 1:
            adjacent_availability = self.check_adjacent_availability(board, row, col, direction, piece)
            if adjacent_availability == "both":
                return float('inf')  # Unstoppable win
            elif adjacent_availability == "one":
                score += 900000  # Likely win
            else:
                score += 0  # No promising future

        # Feature 3: Two connected (3 situations)
        if count_piece == 2 and count_empty == 2:
            available_squares = self.count_available_squares(board, row, col, direction)
            if available_squares >= 5:
                score += 40000  # Left Situation (most promising future)
            elif available_squares == 4:
                score += 30000  # Middle Situation (moderate future)
            elif available_squares == 3:
                score += 20000  # Right Situation (less promising)
            elif available_squares == 2:
                score += 10000  # Least favorable but still valid

        # Block opponent's three connected
        if count_opp_piece == 3 and count_empty == 1:
            score -= 900000

        # Ensure a score is always returned
        return score

    def check_adjacent_availability(self, board, row, col, direction, piece):
        # Check the availability of adjacent spaces for a horizontal 3-connected pattern.
        ROWS = self.num_rows
        COLS = self.num_cols
        if direction != 'horizontal':
            return None  # Adjacent availability checks only apply to horizontal connections

        left_empty = col > 0 and board[row][col - 1] == EMPTY
        right_empty = col + 3 < COLS - 1 and board[row][col + 4] == EMPTY

        if left_empty and right_empty:
            return "both"
        elif left_empty or right_empty:
            return "one"
        else:
            return "none"

    def count_available_squares(self, board, row, col, direction):
        # Count the number of available squares adjacent to two connected chessmen.
        ROWS = self.num_rows
        COLS = self.num_cols
        available = 0

        if direction == 'horizontal':
            # Check left and right along the row
            for c in range(col - 1, -1, -1):
                if board[row][c] == EMPTY:  # Fixed indexing
                    available += 1
                else:
                    break
            for c in range(col + 4, COLS):
                if board[row][c] == EMPTY:  # Fixed indexing
                    available += 1
                else:
                    break

        elif direction == 'vertical':
            # Check downward along the column
            for r in range(row + 2, ROWS):
                if board[r][col] == EMPTY:  # Fixed indexing
                    available += 1
                else:
                    break

        elif direction == 'positive_diagonal' or direction == 'negative_diagonal':
            # Implement diagonal checks if necessary
            pass

        return available

    def single_piece_heuristic(self, board, piece):
        # Evaluate single chessmen based on their position on the board.
        ROWS = self.num_rows
        COLS = self.num_cols
        position_values = [40, 70, 120, 200, 120, 70, 40]  # Column-wise values for single pieces
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == piece:
                    score += position_values[col]
                elif board[row][col] == (PLAYER_PIECE if piece == AI_PIECE else AI_PIECE):
                    score -= position_values[col]
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
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 'X'
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
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

    def post_scores(self):
        """Display the scores."""
        print(f"Player 1 score: {self.scores[0]} | Player 2 score: {self.scores[1]}")

    def play_game(self):
        count = 0
        """Play the game."""
        while True:
            self.print_board()

            if not self.get_valid_moves():
                print("game over")
                break

            # Player's turn
            self.player_turn()
            self.post_scores()
            self.save_and_encode_tree()
            self.decode_and_print_tree()

            # AI's turn
            self.computer_turn()
            self.post_scores()


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=4)
    game.play_game()
