import numpy as np
import random

# Game constants
ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER_ONE = 1  # User
PLAYER_TWO = 2  # Minimax AI
MAX_DEPTH = 4  # Set a reasonable depth for the search

# Heuristic function
def Heuristics2(r, c):
    M = np.zeros((r, c), dtype=int)
    cr = r // 2
    cc = c // 2
    for i in range(r):
        for j in range(c):
            d = abs(i - cr) + abs(j - cc)
            M[i][j] = (r + c) - d
    return M

# Initialize the heuristic matrix
heuristic_matrix = Heuristics2(ROWS, COLUMNS)

def is_full(board):
    """Check if the board is full."""
    return all(board[r][c] != EMPTY for r in range(ROWS) for c in range(COLUMNS))

def get_valid_moves(board):
    """Get the list of columns where a move can be made."""
    return [c for c in range(COLUMNS) if board[0][c] == EMPTY]

def make_move(board, col, player):
    """Make a move on the board (drop a piece in the chosen column)."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return r, col
    return None

def undo_move(board, row, col):
    """Undo a move by resetting the position."""
    board[row][col] = EMPTY

def minimax(board, depth, maximizing_player):
    """Minimax algorithm to find the best move."""
    valid_moves = get_valid_moves(board)

    if depth == 0 or is_full(board):
        # Return heuristic evaluation if no winner or full board
        return evaluate_board(board)

    if maximizing_player:
        best_value = -float('inf')
        for col in valid_moves:
            row, col = make_move(board, col, PLAYER_TWO)
            value = minimax(board, depth - 1, False)  # Minimize for Player 1
            best_value = max(best_value, value)
            undo_move(board, row, col)
        return best_value
    else:
        best_value = float('inf')
        for col in valid_moves:
            row, col = make_move(board, col, PLAYER_ONE)
            value = minimax(board, depth - 1, True)  # Maximize for Player 2
            best_value = min(best_value, value)
            undo_move(board, row, col)
        return best_value

def evaluate_board(board):
    """Evaluate the board using the heuristic matrix."""
    score = 0
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == PLAYER_ONE:
                score += heuristic_matrix[r][c]
            elif board[r][c] == PLAYER_TWO:
                score -= heuristic_matrix[r][c]
    return score

def best_move(board):
    """Find the best move for the current player (using Minimax)."""
    valid_moves = get_valid_moves(board)
    best_value = -float('inf')
    best_col = random.choice(valid_moves)
    
    for col in valid_moves:
        row, col = make_move(board, col, PLAYER_TWO)  # Try Player 2's move
        move_value = minimax(board, MAX_DEPTH, False)  # Minimize for Player 1
        if move_value > best_value:
            best_value = move_value
            best_col = col
        undo_move(board, row, col)
    
    return best_col

# Initialize a blank board
board = np.zeros((ROWS, COLUMNS), dtype=int)

# Example of running the game with User Input and Minimax AI
def run_game():
    current_player = PLAYER_ONE  # User starts
    while not is_full(board):  # Game ends when board is full
        if current_player == PLAYER_ONE:
            # Player 1 (User) input
            print_board(board)
            move = int(input("Player 1, choose a column (1-7): ")) - 1  # Adjust input for 0-based indexing
            while move not in get_valid_moves(board):
                print("Invalid move. Try again.")
                move = int(input("Player 1, choose a column (1-7): ")) - 1
            row, col = make_move(board, move, PLAYER_ONE)
            print(f"Player 1 places at ({row + 1}, {col + 1})")  # Adjust for 1-based display
            current_player = PLAYER_TWO  # Switch to Player 2
        else:
            # Player 2 (Minimax AI) makes a move
            move = best_move(board)
            row, col = make_move(board, move, PLAYER_TWO)
            print(f"Player 2 places at ({row + 1}, {col + 1})")  # Adjust for 1-based display
            current_player = PLAYER_ONE  # Switch to Player 1
        print_board(board)

    print("The board is full. It's a draw!")
    print_board(board)

def print_board(board):
    """Print the current game board."""
    for r in range(ROWS):
        print(' | '.join(str(board[r][c]) for c in range(COLUMNS)))
        print('-' * (COLUMNS * 4 - 1))
    print("  ".join(str(i + 1) for i in range(COLUMNS)))  # Add column numbers (1-7) below the board

# Run the game
run_game()
