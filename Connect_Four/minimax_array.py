def minimax(board, depth, maximizing_player):
    valid_moves = get_valid_moves(board)
    if depth == 0 or len(valid_moves) == 0:
        return None, heuristic(board, AI_PIECE)

    if maximizing_player:
        value = -float('inf')
        best_col = None
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            b, score = minimax(temp_board, depth - 1, False)
            if score > value:
                value = score
                best_col = col
        return best_col, value
    else:
        value = float('inf')
        best_col = None
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            b2, score = minimax(temp_board, depth - 1, True)
            if score < value:
                value = score
                best_col = col
        return best_col, value
