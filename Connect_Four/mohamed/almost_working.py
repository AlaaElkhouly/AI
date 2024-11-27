
import math

class ConnectFour:
    def __init__(self, max_depth=2):
        self.player1_board = 0b0  # bitboard for player 1
        self.player2_board = 0b0   # bitboard for player 2
        self.height = [0] * 7   # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.queue=[]
        self.scores=[0,0] # store player one and player two scores after each move

    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]
    
    def save_and_encode_tree(self):
        # Combine the bitboards into one and save to the queue
        combined_board = (self.player2_board<< 1) | self.player1_board
        self.queue.append(combined_board)

    def decode_and_print_tree(self):
        queue=self.queue
        rows=self.num_rows
        cols=self.num_cols
        # Iterate through each node in the queue
        for node_index, combined_board in enumerate(queue):
            print(f"Node {node_index}:")
            
            # Create an empty board to display
            board = [[' ' for _ in range(cols)] for _ in range(rows)]
            
            # Decode the bitboard into the board representation
            for col in range(cols):
                for row in range(rows):
                    bit_position = (col * rows) + row
                    # Extract the two bits for the current cell
                    cell_value = (combined_board >> (bit_position * 2)) & 0b11

                    # Map the cell value to the appropriate symbol
                    if cell_value == 0b01:  # Player 1
                        board[row][col] = 'X'
                    elif cell_value == 0b10:  # Player 2
                        board[row][col] = 'O'

            # Print the board (flip vertically so the bottom row is printed last)
            for row in reversed(board):
                print('|' + '|'.join(row) + '|')
            print()  # Add a blank line between boards

    def drop_piece(self, player_bitboard, column):
        """Simulate dropping a piece in the given column."""
        if self.height[column] >= self.num_rows:
            raise ValueError("Column is full!")
        mask = 1 << (column * 7 + self.height[column])
        player_bitboard |= mask
        self.height[column] += 1
        self.save_and_encode_tree()                             #save each node
        return player_bitboard


    def undo_drop_piece(self, player_bitboard, column):
        """Undo the last piece drop."""
        self.height[column] -= 1
        mask = 1 << (column * 7 + self.height[column])
        player_bitboard &= ~mask
        return player_bitboard

    def evaluate_board(self):
        """Evaluate the current board state for scoring."""
        directions = [1, 6, 7, 8]
        player1_score = 0
        player2_score = 0

        for direction in directions:
            for shift in [1, 2, 3]:  # Look for streaks of 2, 3, or 4
                player1_temp = self.player1_board & (self.player1_board >> direction)
                player2_temp = self.player2_board & (self.player2_board >> direction)
                
                player1_score += shift * bin(player1_temp & (player1_temp >> (shift * direction))).count('1')
                player2_score += shift * bin(player2_temp & (player2_temp >> (shift * direction))).count('1')

        self.scores=[player1_score,player2_score]
        return  player1_score - player2_score


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
                if (self.player1_board >> (col * 7 + row)) & 1:
                    board[row][col] = 'X'
                elif (self.player2_board >> (col * 7 + row)) & 1:
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
        print(f"player one score is{self.scores[0]}..... player two score is{self.scores[1]}")

    def play_game(self):
        """Play the game."""
        while True:
            self.print_board()

            # Check for tie
            if len(self.get_valid_moves()) == 0:
                print("It's a tie!")
                break

            # Player's turn
            self.player_turn()
            
            # post the scores
            self.post_scores()
            
            #print tree 
            self.decode_and_print_tree()
            
             # post the scores
            self.post_scores()

            # AI's turn
            self.computer_turn()


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=5)
    game.play_game()
