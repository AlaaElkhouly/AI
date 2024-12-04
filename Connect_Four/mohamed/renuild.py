import math
from anytree import NodeMixin, RenderTree, Node
import numpy as np


class ConnectFour(NodeMixin):
    def __init__(self, max_depth=4):
        self.player1_board = 0b0  # Bitboard for player 1 player is ai
        self.player2_board = 0b0  # Bitboard for player 2
        self.column_heights = [0] * 7  # Column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.scores = [0, 0]  # Scores for player 1 and player 2
        self.k = 1  # Max depth for the tree search
        self.tree_root = Node("Root")
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2 
        self.COLS = self.num_cols
        self.ROWS = self.num_rows
        self.EMPTY = 0

##------------------------------------------    Board Operations------------------------------------------------##
    def get_valid_moves(self):
        """Return list of valid columns (where a piece can be dropped)."""
        return [col for col in range(self.num_cols) if self.column_heights[col] < self.num_rows]

    def drop_piece(self, player_bitboard, column):
        """Simulate dropping a piece in the given column."""
        if self.column_heights[column] >= self.num_rows:
            raise ValueError("Column is full!")
        mask = 1 << (column * self.num_rows + self.column_heights[column])
        player_bitboard |= mask
        self.column_heights[column] += 1
        return player_bitboard

    def undo_drop_piece(self, player_bitboard, column):
        """Undo the last piece drop."""
        self.column_heights[column] -= 1
        mask = 1 << (column * self.num_rows + self.column_heights[column])
        player_bitboard &= ~mask
        return player_bitboard
    

##---------------------------------------------heuristics---------------------------------------------------------##

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

    def bitboard_to_array(self, rows, cols):
        board = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 1
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 2
        #print(board)
        return board

    def heuristic(self, bitboard, piece):
        ROWS = self.num_rows
        COLS = self.num_cols
        board=self.bitboard_to_array(ROWS,COLS)
        #print(board)
        score = 0
        opp_piece = self.PLAYER_PIECE if piece == self.AI_PIECE else self.AI_PIECE

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
        opp_piece = self.PLAYER_PIECE if piece == self.AI_PIECE else self.AI_PIECE

        count_piece = np.count_nonzero(np.array(window) == piece)
        count_empty = np.count_nonzero(np.array(window) == self.EMPTY)
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

        left_empty = col > 0 and board[row][col - 1] == self.EMPTY
        right_empty = col + 3 < COLS - 1 and board[row][col + 4] == self.EMPTY

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
                if board[row][c] == self.EMPTY:
                    available += 1
                else:
                    break
            for c in range(col + 4, COLS):
                if board[row][c] == self.EMPTY:
                    available += 1
                else:
                    break

        elif direction == 'vertical':
            # Check downward along the column
            for r in range(row + 2, ROWS):
                if board[r][col] == self.EMPTY:
                    available += 1
                else:
                    break

        elif direction == 'positive_diagonal':
            # Check positive diagonal (\ direction)
            # Check bottom-left
            r, c = row + 2, col - 2
            while r < ROWS and c >= 0:
                if board[r][c] == self.EMPTY:
                    available += 1
                else:
                    break
                r += 1
                c -= 1
            # Check top-right
            r, c = row - 2, col + 2
            while r >= 0 and c < COLS:
                if board[r][c] == self.EMPTY:
                    available += 1
                else:
                    break
                r -= 1
                c += 1

        elif direction == 'negative_diagonal':
            # Check negative diagonal (/ direction)
            # Check bottom-right
            r, c = row + 2, col + 2
            while r < ROWS and c < COLS:
                if board[r][c] == self.EMPTY:
                    available += 1
                else:
                    break
                r += 1
                c += 1
            # Check top-left
            r, c = row - 2, col - 2
            while r >= 0 and c >= 0:
                if board[r][c] == self.EMPTY:
                    available += 1
                else:
                    break
                r -= 1
                c -= 1

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
                #elif board[row][col] == (self.PLAYER_PIECE if piece == self.AI_PIECE else self.AI_PIECE):
                 #    score -= position_values[col]
              
        return score

    def evaluate_board(self):
       # player_score = self.heuristic(self.player1_board, self.PLAYER_PIECE)
        ai_score = self.heuristic(self.player1_board, self.AI_PIECE)
        player_score=self.heuristic(self.player2_board, self.PLAYER_PIECE)
        self.scores = [ai_score,player_score]
        #print(f"Debug: Player score = {player_score}, AI score = {ai_score}")
        return ai_score


##----------------------------------------------calculate utility--------------------------------------------##






##-----------------------------------------------tree printing-----------------------------------------------##
    def generate_board_string(self):
            connect_four_board = ["."] * 42  # Use a list for the board visualization
            score=self.evaluate_board()

            # Visualize the bitboard state
            for i in range(42):
                if self.player1_board & (1 << i):  # Check if the i-th bit is set for Player 1
                    connect_four_board[i] = 'X'
                elif self.player2_board & (1 << i):  # Check if the i-th bit is set for Player 2
                    connect_four_board[i] = 'O'
                else:
                    connect_four_board[i] = '.'  # Empty space
            str_board="".join(connect_four_board)
            printed=str_board 
            return(printed)

    def print_tree(self):
            """Print the tree using anytree's RenderTree."""
            if not self.root_node:
                print("Tree has not been created yet.")
                return
            for pre, _, node in RenderTree(self.root_node):
                print(f"{pre}{node.name}: Depth {node.depth}")
                print(node.board)
                print()

    def display_tree(self):
        for pre, fill, node in RenderTree(self.tree_root):
            print(f"{pre}{node.name}")

    def print_board_for_player(self):
        """Visualize the current board."""
        board = [[' ' for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.column_heights[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 'X'
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = 'O'
        for row in reversed(board):
            print('|' + '|'.join(row) + '|')

##-----------------------------------------------------------minimax-------------------------------------------------------------------------------------###
    def minimax(self, depth, alpha, beta, maximizing_player, parent_node=None):
        if depth == 0 or not self.get_valid_moves():
            score = self.evaluate_board()
            # Attach leaf node with score
            Node(f"score: {score}", parent=parent_node)
            return score, None

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            max_value = -math.inf
            for column in valid_moves:
                self.player1_board = self.drop_piece(self.player1_board, column)
                board_string= self.generate_board_string()
                
                # Create child node
                child_node = Node(f"(Max) Move: {column} ,board: {board_string} ", parent=parent_node)
                
                value, _ = self.minimax(depth - 1, alpha, beta, False, child_node)
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
                board_string= self.generate_board_string()

                # Create child node
                child_node = Node(f"(Min)Move: {column}, board: {board_string} ", parent=parent_node)

                value, _ = self.minimax(depth - 1, alpha, beta, True, child_node)
                self.player2_board = self.undo_drop_piece(self.player2_board, column)

                if value < min_value:
                    min_value = value
                    best_move = column

                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_value, best_move

##-------------------------------------------------------------------gameplay--------------------------------------------------------------##
        
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
        self.player2_board = self.drop_piece(self.player2_board, move)

    def computer_turn(self):
        print("AI is thinking...")
        self.tree_root = Node("Root")  # Reset the tree for this turn
        _, move = self.minimax(self.max_depth, float('-inf'), float('inf'), True, self.tree_root)
        print(f"AI chooses column {move}")
        self.player1_board = self.drop_piece(self.player1_board, move)
        self.display_tree()  # Display the tree after the AI move

    def play_game(self):
        """Play the game."""
        while True:
            self.print_board_for_player()

            if not self.get_valid_moves():
                print("Game over!")
                break

            # Player's turn
            self.player_turn()
            

            # AI's turn
            self.computer_turn()
            


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=2)
    game.play_game()
