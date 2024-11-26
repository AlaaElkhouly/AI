def bitboard_to_array(bitboard, rows, cols):
    board = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            bit_position = i * cols + j
            board[i, j] = (bitboard >> bit_position) & 1
    return board
 
def heuristic(bitboard, piece):
     board = bitboard_to_array(bitboard, ROWS, COLS)
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # Feature 1: Absolute win
    if check_win(board, piece):
        return float('inf')  # AI wins
    if check_win(board, opp_piece):
        return float('-inf')  # Opponent wins

    # Horizontal scoring
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row, col:col + 4]
            score += evaluate_window_heuristic1(window, piece, row, col, direction='horizontal')

    # Vertical scoring
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row + 4, col]
            score += evaluate_window_heuristic1(window, piece, row, col, direction='vertical')

    # Positive diagonal scoring
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i, col + i] for i in range(4)]
            score += evaluate_window_heuristic1(window, piece, row, col, direction='positive_diagonal')

    # Negative diagonal scoring
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i, col + i] for i in range(4)]
            score += evaluate_window_heuristic1(window, piece, row, col, direction='negative_diagonal')

    # Feature 4: Single chessmen position evaluation
    score += single_piece_heuristic(board, piece)

    return score
 
def evaluate_window_heuristic1(window, piece, row, col, direction):
    
    #Evaluate a window of 4 cells for Heuristic-1 features.
 
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    count_piece = np.count_nonzero(window == piece)
    count_empty = np.count_nonzero(window == EMPTY)
    count_opp_piece = np.count_nonzero(window == opp_piece)

    # Feature 1: Absolute win
    if count_piece == 4:
        return float('inf')  # Absolute win

    # Feature 2: Three connected chessmen
    if count_piece == 3 and count_empty == 1:
        adjacent_availability = check_adjacent_availability(board, row, col, direction, piece)
        if adjacent_availability == "both":
            return float('inf')  # Unstoppable win
        elif adjacent_availability == "one":
            score += 900000  # Likely win
        else:
            score += 0  # No promising future

    # Feature 3: Two connected chessmen
    if count_piece == 2 and count_empty == 2:
        available_squares = count_available_squares(board, row, col, direction)
        if available_squares >= 5:
            score += 40000
        elif available_squares == 4:
            score += 30000
        elif available_squares == 3:
            score += 20000
        elif available_squares == 2:
            score += 10000

    # Block opponent's three connected
    if count_opp_piece == 3 and count_empty == 1:
        score -= 900000

    return score
 
def check_adjacent_availability(board, row, col, direction, piece):
    
    #Check the availability of adjacent spaces for a horizontal 3-connected pattern.

    if direction != 'horizontal':
        return None  # Adjacent availability checks only apply to horizontal connections

    left_empty = col > 0 and board[row, col - 1] == EMPTY
    right_empty = col + 3 < COLS - 1 and board[row, col + 4] == EMPTY

    if left_empty and right_empty:
        return "both"
    elif left_empty or right_empty:
        return "one"
    else:
        return "none"

 
def count_available_squares(board, row, col, direction):

   # Count the number of available squares adjacent to two connected chessmen.

    available = 0

    if direction == 'horizontal':
        # Check left and right along the row
        for c in range(col - 1, -1, -1):
            if board[row, c] == EMPTY:
                available += 1
            else:
                break
        for c in range(col + 4, COLS):
            if board[row, c] == EMPTY:
                available += 1
            else:
                break

    elif direction == 'vertical':
        # Check downward along the column
        for r in range(row + 2, ROWS):
            if board[r, col] == EMPTY:
                available += 1
            else:
                break

    elif direction == 'positive_diagonal' or direction == 'negative_diagonal':
        # Implement diagonal checks if necessary
        pass

    return available
 
def single_piece_heuristic(board, piece):
    
    #Evaluate single chessmen based on their position on the board.
   
    position_values = [40, 70, 120, 200, 120, 70, 40]  # Column-wise values for single pieces
    score = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board[row, col] == piece:
                score += position_values[col]
            elif board[row, col] == (PLAYER_PIECE if piece == AI_PIECE else AI_PIECE):
                score -= position_values[col]
    return score
