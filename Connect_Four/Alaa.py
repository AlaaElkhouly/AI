import numpy as np
import random
#_____________________________________________________________________________________________#
def Heuristics2(r, c):
    M = np.zeros((r, c), dtype=int)
    cr = r // 2
    cc = c // 2
    for i in range(r):
        for j in range(c):
            d = abs(i - cr) + abs(j - cc)
            M[i][j] = (r + c) - d
    return M
#_____________________________________________________________________________________________#
def is_valid_move(board, col):
    return board[0][col] == 0
#_____________________________________________________________________________________________#

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            return row
#_____________________________________________________________________________________________#
def drop_piece(board, row, col, piece):
    board[row][col] = piece
#_____________________________________________________________________________________________#
def evaluate_board(board, piece):
    opponent_piece = 1 if piece == 2 else 2
    return np.sum(board * HEURISTIC_MATRIX) if piece else -np.sum(board * HEURISTIC_MATRIX)
#_____________________________________________________________________________________________#
def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]
#_____________________________________________________________________________________________#
def minimax(board, depth, maximizingPlayer, piece):
    valid_moves = get_valid_moves(board)
    if depth == 0 or not valid_moves:
        return None, evaluate_board(board, piece)
    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() # i think copy here is useless
            drop_piece(temp_board, row, col, piece) # isnt piece here always 1?
            _, score = minimax(temp_board, depth - 1, False, piece) # mish true w false el 3ks?
            if score > value:
                value = score
                best_col = col
        return best_col, value
    else:
        value = np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() # i think copy here is useless
            drop_piece(temp_board, row, col, 1 if piece == 2 else 2) # isnt piece here always 2?
            _, score = minimax(temp_board, depth - 1, True, piece) # mish true w false el 3ks?
            if score < value:
                value = score
                best_col = col
        return best_col, value
#_____________________________________________________________________________________________#
def alpha_beta_pruning(board, depth, alpha, beta, maximizingPlayer, piece):
    valid_moves = get_valid_moves(board)
    if depth == 0 or not valid_moves:
        return None, evaluate_board(board, piece)
    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() # i think copy here is useless
            drop_piece(temp_board, row, col, piece) # isnt piece here always 1?
            _, score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, False, piece) # mish true w false el 3ks?
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() # i think copy here is useless
            drop_piece(temp_board, row, col, 1 if piece == 2 else 2) # isnt piece here always 2?
            _, score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, True, piece) # mish true w false el 3ks?
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value
#_____________________________________________________________________________________________#
def expected_minimax(board, depth, piece, prob=0.6):
    valid_moves = get_valid_moves(board)
    if depth == 0 or not valid_moves:
        return None, evaluate_board(board, piece)
    value = 0
    best_col = random.choice(valid_moves)
    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy() # i think copy here is useless
        drop_piece(temp_board, row, col, piece)
        _, score = minimax(temp_board, depth - 1, False, piece)
        value += prob * score
    return best_col, value
#_____________________________________________________________________________________________#
def play_game():
    ROWS = 6
    COLS = 7
    depth = 3
    HEURISTIC_MATRIX = Heuristics2(ROWS, COLS)
    numofmoves=int(input("Please Enter Number of moves to be played:"))
    print("Select Mode:")
    print("1. Minimax")
    print("2. Minimax with Alpha-Beta Pruning")
    print("3. Expected Minimax")
    mode = int(input("Enter mode: "))
    board = np.zeros((ROWS, COLS), dtype=int)
    game_over = False
    turn = 0

    while not game_over and turn < numofmoves:
        if turn % 2 == 0:
            col = int(input("Your turn! Enter column (0-6): "))
            if is_valid_move(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                if check_win(board, 1):
                    print("You win!")
                    game_over = True
        else:
            if mode == 1:
                col, _ = minimax(board, depth, True, 2)
            elif mode == 2:
                col, _ = alpha_beta_pruning(board, depth, -np.inf, np.inf, True, 2)
            elif mode == 3:
                col, _ = expected_minimax(board, depth, 2)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            print(f"AI chose column {col}")
            if check_win(board, 2):
                print("AI wins!")
                game_over = True
        
        print(board)
        turn += 1
    
    if not game_over:
        print("Game over! Max turns reached.")
#_____________________________________________________________________________________________#
play_game()