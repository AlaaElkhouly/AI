import math
from anytree import NodeMixin, RenderTree, Node

class ConnectFour(NodeMixin):
    def __init__(self, max_depth=4):
        self.player1_board = 0b0  # Bitboard for player 1
        self.player2_board = 0b0  # Bitboard for player 2
        self.column_heights = [0] * 7  # Column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.scores = [0, 0]  # Scores for player 1 and player 2
        self.k = 1  # Max depth for the tree search
        self.tree_root = Node("Root")  

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

    def evaluate_board(self):
        """Evaluate the board state and calculate scores for both players."""
        directions = [1, 7, 8, 6]  # Right, Up-Left, Up, Up-Right
        player1_score, player2_score = 0, 0

        for direction in directions:
            for shift in range(1, 4):  # Check streaks of 2, 3, and 4
                player1_temp = self.player1_board & (self.player1_board >> direction)
                player2_temp = self.player2_board & (self.player2_board >> direction)
                player1_score += bin(player1_temp & (player1_temp >> (shift * direction))).count("1") * shift
                player2_score += bin(player2_temp & (player2_temp >> (shift * direction))).count("1") * shift

        self.scores = [player1_score, player2_score]
        return player1_score - player2_score

    def save_and_encode_tree(self, current_depth=0, parent=None):
        """Save the game state into the tree using anytree."""
        if parent is None:
            board_string = self.generate_board_string()
            self.root_node = Node("Root", depth=current_depth, board=board_string)
            parent = self.root_node

        if current_depth >= self.k:
            return  # Stop if max depth is reached

        valid_moves = self.get_valid_moves()
        for column in valid_moves:
            # Simulate dropping a piece for player 1
            self.player1_board = self.drop_piece(self.player1_board, column)
            self.save_and_encode_tree(current_depth + 1, parent)
            self.player1_board = self.undo_drop_piece(self.player1_board, column)

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

    def print_board(self):
        """Print the current board."""
        print(self.generate_board_string())

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


    def post_scores(self):
        """Display the scores."""
        print(f"computer score: {self.scores[0]} | Player 2 score: {self.scores[1]}")

    def play_game(self):
        """Play the game."""
        while True:
            self.print_board_for_player()

            if not self.get_valid_moves():
                print("Game over!")
                break

            # Player's turn
            self.player_turn()
            self.post_scores()

            # AI's turn
            self.computer_turn()
            


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=2)
    game.play_game()
