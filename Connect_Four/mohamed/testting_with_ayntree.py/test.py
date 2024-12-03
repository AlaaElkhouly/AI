import math
from anytree import NodeMixin, RenderTree


class ConnectFour(NodeMixin):
    def __init__(self, max_depth=4):
        self.player1_board = 0b0  # bitboard for player 1
        self.player2_board = 0b0  # bitboard for player 2
        self.height = [0] * 7  # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.scores = [0, 0]  # scores for player 1 and player 2
        self.k = 4
        self.root_node = None  # Root of the tree
        self.current_parent = None  # Current node during exploration

    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]

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

    def save_and_encode_tree(self, current_depth=0, parent=None):
        """Save the game state into the tree using anytree."""
        board_string = self.generate_board_string()
        if parent is None:
            # Create root node if this is the first call
            self.root_node = NodeMixin("Root", depth=current_depth, board=board_string)
            parent = self.root_node
        else:
            # Create a child node under the given parent
            parent = NodeMixin(f"Node_{current_depth}", depth=current_depth, board=board_string, parent=parent)

        if current_depth >= self.max_depth:
            return  # Stop if maximum depth is reached

        # Generate children by simulating moves
        valid_moves = self.get_valid_moves()
        for column in valid_moves:
            # Temporarily drop a piece for player 2
            self.player2_board = self.drop_piece(self.player2_board, column)
            self.save_and_encode_tree(current_depth + 1, parent)
            self.player2_board = self.undo_drop_piece(self.player2_board, column)

    def generate_board_string(self):
        """Generate a string representation of the current board."""
        board = [["." for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = "X"
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = "O"
        return "\n".join("".join(row) for row in reversed(board))

    def print_tree(self):
        """Print the tree using anytree's RenderTree."""
        if not self.root_node:
            print("Tree has not been created yet.")
            return
        for pre, _, node in RenderTree(self.root_node):
            print(f"{pre}{node.name}: Depth {node.depth}")
            print(node.board)
            print()

    def evaluate_board(self):
        """Evaluate the board state to calculate scores."""
        directions = [1, 7, 8, 6]  # Right, Up-Left, Up, Up-Right
        player1_score = 0
        player2_score = 0

        for direction in directions:
            for shift in range(1, 4):  # Check streaks of 2, 3, and 4
                player1_temp = self.player1_board & (self.player1_board >> direction)
                player2_temp = self.player2_board & (self.player2_board >> direction)
                player1_score += bin(player1_temp & (player1_temp >> (shift * direction))).count("1") * shift
                player2_score += bin(player2_temp & (player2_temp >> (shift * direction))).count("1") * shift

        self.scores = [player1_score, player2_score]
        return player1_score - player2_score

    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax with alpha-beta pruning."""
        if depth == 0 or not self.get_valid_moves():
            return self.evaluate_board(), None

        if depth >= self.max_depth - self.k:
            self.save_and_encode_tree()

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
        board = [[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.height[col]):
                if (self.player1_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = "X"
                elif (self.player2_board >> (col * self.num_rows + row)) & 1:
                    board[row][col] = "O"
        for row in reversed(board):
            print("|" + "|".join(row) + "|")

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
        _, move = self.minimax(self.max_depth, float("-inf"), float("inf"), True)
        print(f"AI chooses column {move}")
        self.player2_board = self.drop_piece(self.player2_board, move)

    def play_game(self):
        """Play the game."""
        while True:
            self.print_board()

            if not self.get_valid_moves():
                print("Game over!")
                break

            # Player's turn
            self.player_turn()

            # AI's turn
            self.computer_turn()

            # Print the game tree after AI's move
            self.print_tree()


if __name__ == "__main__":
    game = ConnectFour(max_depth=4)
    game.play_game()
