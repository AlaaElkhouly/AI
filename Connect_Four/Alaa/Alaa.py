import numpy as np
import random
ROWS = 6
COLS = 7
depth = 3
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
HEURISTIC_MATRIX = Heuristics2(ROWS, COLS)                                                                                                                                                                                                                                                                                      
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
def minimax2(board, depth, maximizingPlayer, piece):
    valid_moves = get_valid_moves(board)
    if depth == 0 or not valid_moves:
        return None, evaluate_board(board, piece)
    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() 
            drop_piece(temp_board, row, col, piece) # isnt piece here always 1?
            _, score = minimax2(temp_board, depth - 1, False, piece)
            if score > value:
                value = score
                best_col = col
        return best_col, value
    else:
        value = np.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy() 
            drop_piece(temp_board, row, col, 1 if piece == 2 else 2) # isnt piece here always 2?
            _, score = minimax2(temp_board, depth - 1, True, piece)
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
            temp_board = board.copy() 
            drop_piece(temp_board, row, col, piece) # isnt piece here always 1?
            _, score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, False, piece)
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
            temp_board = board.copy() 
            drop_piece(temp_board, row, col, 1 if piece == 2 else 2) # isnt piece here always 2?
            _, score = alpha_beta_pruning(temp_board, depth - 1, alpha, beta, True, piece)
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
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        _, score = minimax2(temp_board, depth - 1, False, piece)
        value += prob * score
    return best_col, value
#_____________________________________________________________________________________________#
def play_game():
    numofmoves=int(input("Please Enter Number of moves to be played:"))
    print("Select Mode:\n1. Minimax\n2. Minimax with Alpha-Beta Pruning\n3. Expected Minimax\n")
    mode = int(input("Enter mode: "))
    board = np.zeros((ROWS, COLS), dtype=int)
    turn = 0
    while   np.sum(board == 0)!=0 and turn < numofmoves:
        if turn % 2 == 0:
            col = int(input("Your turn! Enter column (0-6): "))
            if is_valid_move(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
        else:
            if mode == 1:
                col, _ = minimax2(board, depth, True, 2)
            elif mode == 2:
                col, _ = alpha_beta_pruning(board, depth, -np.inf, np.inf, True, 2)
            elif mode == 3:
                col, _ = expected_minimax(board, depth, 2)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            print(f"AI chose column {col}")
        print(board)
        turn += 1
    print("Game over!")
    print("score is",(np.sum(HEURISTIC_MATRIX[board==1])-np.sum(HEURISTIC_MATRIX[board==2])))
#_____________________________________________________________________________________________#
play_game()
'''
My Notes:
1) board.copy() ensures the original board remains unchanged during recursive evaluations.

2) In drop_piece(temp_board, row, col, piece), isn't piece always equal to 1 or 2?
    In the function, piece represents the piece of the maximizing player (Player 1). During the
    maximizing player's turn, piece is passed as-is to simulate their move.But during the minimizing
    player's turn, piece is used to determine the opponent's piece (which is 2 for the AI, assuming
    Player 1 is maximizing). This distinction is maintained in the code by swapping the piece in the
    minimizing player block using 1 if piece == 2 else 2.

3) During the maximizing player's turn (maximizingPlayer = True), the recursive call to minimax for the
   next depth passes False for maximizingPlayer, as the next turn belongs to the minimizing player and vice versa.

1.check my green comments with chat gpt
2.Redo expected minimax
3.create a tree for each mode
4. link with GUI
5 create Report
'''
#_____________________________________________________________________________________________#
import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
ROWS = 6
COLUMNS = 7
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 10

# Colors and themes
THEMES = {
    "Classic": {"bg": (0, 0, 139), "player1": (255, 0, 0), "player2": (255, 255, 0)},
    "Ocean": {"bg": (0, 105, 148), "player1": (255, 128, 0), "player2": (255, 255, 102)},
    "Forest": {"bg": (34, 139, 34), "player1": (255, 69, 0), "player2": (154, 205, 50)},
    "Gray": {"bg": (169, 169, 169), "player1": (255, 255, 255), "player2": (70, 70, 70)},
}

current_theme = "Classic"
BACKGROUND_COLOR = THEMES[current_theme]["bg"]
PLAYER_ONE_COLOR = THEMES[current_theme]["player1"]
PLAYER_TWO_COLOR = THEMES[current_theme]["player2"]
EMPTY_COLOR = (30, 30, 30)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
pygame.display.set_caption("Connect Four")

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# Game state
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = 1
dropdown_active = False
minimax_mode = 0  # 0: "Without α-β", 1: "With α-β", 2: "Expected"
heuristic_mode = 1  # 1 or 2


def Wh1():
    print("Heuristic 1 With α-β")
    return 0


def WOh1():
    print("Heuristic 1 Without α-β")
    return 0


def Eh1():
    print("Heuristic 1 Expected")
    return 0


def Wh2():
    print("Heuristic 2 With α-β")
    return 0


def WOh2():
    print("Heuristic 2 Without α-β")
    return 0


def Eh2():
    print("Heuristic 2 Expected")
    return 0


def draw_board():
    """Draw the game board and pieces."""
    screen.fill((255, 255, 255))  # White background

    # Draw grid and pieces
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, BACKGROUND_COLOR,
                             (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, (0, 0, 0),
                               (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                               RADIUS + 5)

            # Draw pieces
            if board[row][col] == 0:
                color = EMPTY_COLOR
            elif board[row][col] == 1:
                color = PLAYER_ONE_COLOR
            else:
                color = PLAYER_TWO_COLOR
            pygame.draw.circle(screen, color,
                               (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                               RADIUS)


def reset_game():
    """Reset the game board."""
    global board, current_player
    board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = 1


def draw_new_game_button():
    """Draw the New Game button."""
    pygame.draw.rect(screen, (0, 200, 0), (10, 10, 140, 40), border_radius=10)  # Wider button
    label = font.render("New Game", True, (0, 0, 0))
    screen.blit(label, (20, 20))


def draw_theme_dropdown():
    """Draw the theme dropdown menu."""
    pygame.draw.rect(screen, (150, 150, 255), (10, 60, 120, 40), border_radius=10)  # Moved to the left below New Game
    label = font.render("Theme", True, (0, 0, 0))
    screen.blit(label, (30, 70))

    if dropdown_active:
        for i, theme_name in enumerate(THEMES.keys()):
            pygame.draw.rect(screen, (200, 200, 200), (10, 100 + i * 40, 120, 40), border_radius=10)
            theme_label = font.render(theme_name, True, (0, 0, 0))
            screen.blit(theme_label, (20, 110 + i * 40))


def apply_theme(theme_name):
    """Apply the selected theme."""
    global current_theme, BACKGROUND_COLOR, PLAYER_ONE_COLOR, PLAYER_TWO_COLOR
    current_theme = theme_name
    BACKGROUND_COLOR = THEMES[theme_name]["bg"]
    PLAYER_ONE_COLOR = THEMES[theme_name]["player1"]
    PLAYER_TWO_COLOR = THEMES[theme_name]["player2"]


def draw_minimax_toggle():
    """Draw the minimax toggle button."""
    x, y, width, height = SCREEN_WIDTH - 140, 10, 140, 40  # Positioned at the far right
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
    label = small_font.render(f"{['Without α-β', 'With α-β', 'Expected'][minimax_mode]}", True, (0, 0, 0))
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

    # Draw Minimax text
    text_label = font.render("Minimax:", True, (0, 0, 0))
    screen.blit(text_label, (x - 100, y + 10))


def draw_heuristic_toggle():
    """Draw the heuristic toggle button."""
    x, y, width, height = SCREEN_WIDTH - 40, 60, 40, 40  # Positioned at the very right
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
    label = small_font.render(f"{heuristic_mode}", True, (0, 0, 0))
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

    # Draw Heuristic text
    text_label = font.render("Heuristic:", True, (0, 0, 0))
    screen.blit(text_label, (x - 110, y + 10))


def handle_piece_placement(pos):
    """Handle placing a piece on the board."""
    global current_player
    col = pos[0] // CELL_SIZE
    if col >= COLUMNS:
        return
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = current_player
            current_player = 3 - current_player
            return


def is_board_full():
    """Check if the board is full (no empty spaces)."""
    for row in board:
        if 0 in row:
            return False
    return True


# Main game loop
running = True
while running:
    draw_board()
    draw_new_game_button()
    draw_theme_dropdown()
    draw_minimax_toggle()
    draw_heuristic_toggle()

    # Check Minimax and Heuristic modes
    if minimax_mode == 0:
        if heuristic_mode == 1:
            WOh1()
        elif heuristic_mode == 2:
            minimax2()
    elif minimax_mode == 1:
        if heuristic_mode == 1:
            Wh1()
        elif heuristic_mode == 2:
            Wh2()
    elif minimax_mode == 2:
        if heuristic_mode == 1:
            Eh1()
        elif heuristic_mode == 2:
            Eh2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Check New Game button
            if 10 <= pos[0] <= 150 and 10 <= pos[1] <= 50:
                reset_game()

            # Check theme dropdown
            elif 10 <= pos[0] <= 130 and 60 <= pos[1] <= 100:  # Adjusted for left-side position
                dropdown_active = not dropdown_active
            elif dropdown_active and 10 <= pos[0] <= 130:
                for i, theme_name in enumerate(THEMES.keys()):
                    if 100 + i * 40 <= pos[1] < 140 + i * 40:
                        apply_theme(theme_name)
                        dropdown_active = False

            # Check minimax toggle
            elif SCREEN_WIDTH - 140 <= pos[0] <= SCREEN_WIDTH and 10 <= pos[1] <= 50:
                minimax_mode = (minimax_mode + 1) % 3

            # Check heuristic toggle
            elif SCREEN_WIDTH - 40 <= pos[0] <= SCREEN_WIDTH and 60 <= pos[1] <= 100:
                heuristic_mode = 1 if heuristic_mode == 2 else 2

            # Handle piece placement
            elif pos[1] > CELL_SIZE:
                handle_piece_placement(pos)

    pygame.display.update()
