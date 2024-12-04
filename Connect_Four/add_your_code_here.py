import math
from anytree import NodeMixin, RenderTree, Node

class ConnectFour:
    def __init__(self, max_depth):
        self.player1_board = 0b0  # bitboard for player 1
        self.player2_board = 0b0  # bitboard for player 2
        self.height = [0] * 7  # column heights
        self.num_rows = 6
        self.num_cols = 7
        self.max_depth = max_depth
        self.queue = []  # stores nodes for tree visualization
        self.scores = [0, 0]  # scores for player 1 and player 2
        self.k=self.max_depth -1
        self.old_depth=0
        self.count=0
        
        
##get all valid plays from height of board##-----------------------------------------------------
    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.num_cols) if self.height[col] < self.num_rows]



##tree operations##---------------------------------------------------------------------------------   
    def save_and_encode_tree(self, level):
        connect_four_board = ["."] * 42  # Use a list for the board visualization
        valid_moves = self.get_valid_moves()
        score=self.evaluate_board()

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
            str_board="".join(connect_four_board)
            printed=str_board + "         "+ "the depth is " +str(level)+ " levels"+ "the score is "+ str(score)

            # Add the visualized board to the queue
            self.queue.append(printed)
            self.undo_drop_piece(copy_board2,column)
            
    def decode_and_print_tree(self):
        """Decode and display all boards stored in the queue."""
        for node_index, c4_board in enumerate(self.queue):
            print(f"Node {node_index}:")
            print(c4_board)
            print()
            
    def clear_queue(self):
        self.queue.clear()  # Clear previous queue



##drop and undrop piece onto board ##-----------------------------------------------------------------------------
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
    
    

##heuristic function-----------------------------------------------------------------------------------------

                    ###add here ya fares###

##utility evaluation##------------------------------------------------------------------------------------
    def evaluate_board(self):
        """Evaluate the board state to calculate scores."""
        directions = [1, 7, 8, 6]  # Right, Up-Left, Up, Up-Right
        player1_score = 0
        player2_score = 0

        for direction in directions:
            for shift in range(1, 4):  # Check streaks of 2, 3, and 4
                player1_temp = self.player1_board & (self.player1_board >> direction)
                player2_temp = self.player2_board & (self.player2_board >> direction)
                player1_score += bin(player1_temp & (player1_temp >> (shift * direction))).count('1') * shift
                player2_score += bin(player2_temp & (player2_temp >> (shift * direction))).count('1') * shift

        self.scores = [player1_score, player2_score]
        return player1_score - player2_score
    
    


###minimax with alpha beta pruning-------------------------------------------------------------------------
    def minimax(self, depth, alpha, beta, maximizing_player):
        
        """Minimax with alpha-beta pruning."""
        if depth == 0 or not self.get_valid_moves():
            return self.evaluate_board(), None
        
        
        if (depth >= self.max_depth - self.k):
            self.save_and_encode_tree(self.count)


        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            self.count+=1
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
        
        
        
###minimax without alpha beta pruning-------------------------------------------------------------------------
    def minimax_without_alpha_beta(self, depth, maximizing_player):
        """Minimax without alpha-beta pruning."""
        if depth == 0 or not self.get_valid_moves():
            return self.evaluate_board(), None

        # Save the board state if the current depth is within the upper k levels
        if (depth >= self.max_depth - self.k):
            self.save_and_encode_tree(depth)

        valid_moves = self.get_valid_moves()
        best_move = None

        if maximizing_player:
            max_value = -math.inf
            for column in valid_moves:
                self.player1_board = self.drop_piece(self.player1_board, column)
                value, _ = self.minimax_without_alpha_beta(depth - 1, False)  # No alpha-beta parameters
                self.player1_board = self.undo_drop_piece(self.player1_board, column)

                if value > max_value:
                    max_value = value
                    best_move = column

            return max_value, best_move
        else:
            min_value = math.inf
            for column in valid_moves:
                self.player2_board = self.drop_piece(self.player2_board, column)
                value, _ = self.minimax_without_alpha_beta(depth - 1, True)  # No alpha-beta parameters
                self.player2_board = self.undo_drop_piece(self.player2_board, column)

                if value < min_value:
                    min_value = value
                    best_move = column

            return min_value, best_move



### expectiminimax--------------------------------------------------------------------------------------------

            ###add here ya alaa###



###print board for user###--------------------------------------------------------------------------------
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




###player turns  ---> computer is max###-----------------------------------------------------------------------
##max player gets bitbiard1##
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
        """Handle AI's move using Minimax."""
        print("AI is thinking...")
        _, move = self.minimax(self.max_depth, float('-inf'), float('inf'), True)
        print(f"AI chooses column {move}")
        self.player1_board = self.drop_piece(self.player1_board, move)

    def computer_turn_without(self):
        """Handle AI's move using Minimax."""
        print("AI is thinking...")
        _, move = self.minimax_without_alpha_beta(self.max_depth, True)
        print(f"AI chooses column {move}")
        self.player1_board = self.drop_piece(self.player1_board, move)


    def post_scores(self):
        """Display the scores."""
        print(f"Player 1 score: {self.scores[0]} | Player 2 score: {self.scores[1]}")

    def play_game(self):
        count=0
        """Play the game."""
        while True:
            self.print_board()

            if not self.get_valid_moves():
                print("game over")
                break

            # Player's turn
            self.player_turn()
            self.post_scores()
            self.clear_queue()
           
        

            # AI's turn
            self.computer_turn()
            self.post_scores()
            self.decode_and_print_tree()
    
    def play_game_without(self):
        count=0
        """Play the game."""
        while True:
            self.print_board()

            if not self.get_valid_moves():
                print("game over")
                break

            # Player's turn
            self.player_turn()
            self.post_scores()
            self.clear_queue()
        
        

            # AI's turn
            self.computer_turn_without()
            self.post_scores()
            self.decode_and_print_tree()
        
           
            


# Run the game
if __name__ == "__main__":
    game = ConnectFour(max_depth=4)
    game.play_game()
