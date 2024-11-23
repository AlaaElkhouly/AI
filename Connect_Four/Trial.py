import pygame
import sys
import numpy as np
import math

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

# Default theme
current_theme = "Classic"
BACKGROUND_COLOR = THEMES[current_theme]["bg"]
PLAYER_ONE_COLOR = THEMES[current_theme]["player1"]
PLAYER_TWO_COLOR = THEMES[current_theme]["player2"]
EMPTY_COLOR = (30, 30, 30)

# Game settings
PLAYER = 1
AI = 2
DEPTH = 4
WINDOW_LENGTH = 4

# GUI setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
pygame.display.set_caption("Connect Four :)")
font = pygame.font.Font(None, 36)

# Game board
board = np.zeros((ROWS, COLUMNS), dtype=int)
current_player = PLAYER
dropdown_active = False
alpha_beta_pruning = False
game_over = False


# Function to draw the board
def draw_board():
    screen.fill((255, 255, 255))  # White background

    # Draw the top control buttons
    draw_button("New Game", 10, 10, 120, 40, (100, 200, 100))
    draw_button("Restart", 10, 60, 120, 40, (200, 100, 100))
    draw_toggle_button()
    draw_theme_dropdown()

    # Draw the Connect Four board
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, BACKGROUND_COLOR, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, EMPTY_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), RADIUS)

            if board[row][col] == PLAYER:
                pygame.draw.circle(screen, PLAYER_ONE_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), RADIUS)
            elif board[row][col] == AI:
                pygame.draw.circle(screen, PLAYER_TWO_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), RADIUS)


# Function to draw a button
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))


# Function to toggle alpha-beta pruning
def toggle_alpha_beta_pruning():
    global alpha_beta_pruning
    alpha_beta_pruning = not alpha_beta_pruning


# Function to draw the toggle button
def draw_toggle_button():
    x, y, width, height = SCREEN_WIDTH - 120, 20, 80, 40
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=20)
    if alpha_beta_pruning:
        pygame.draw.circle(screen, (0, 255, 0), (x + width - height // 2, y + height // 2), height // 2 - 5)
    else:
        pygame.draw.circle(screen, (255, 0, 0), (x + height // 2, y + height // 2), height // 2 - 5)

    label = font.render("Alpha-Beta", True, (0, 0, 0))
    screen.blit(label, (x - 120, y + 5))


# Function to draw the theme dropdown
def draw_theme_dropdown():
    dropdown_x, dropdown_y, dropdown_w, dropdown_h = (SCREEN_WIDTH - 120) // 2, 20, 120, 40
    pygame.draw.rect(screen, (200, 200, 200), (dropdown_x, dropdown_y, dropdown_w, dropdown_h), border_radius=10)
    label = font.render("Theme", True, (0, 0, 0))
    screen.blit(label, (dropdown_x + 10, dropdown_y + 5))

    if dropdown_active:
        for i, theme in enumerate(THEMES.keys()):
            option_y = dropdown_y + dropdown_h + i * dropdown_h
            pygame.draw.rect(screen, (240, 240, 240), (dropdown_x, option_y, dropdown_w, dropdown_h), border_radius=10)
            option_text = font.render(theme, True, (0, 0, 0))
            screen.blit(option_text, (dropdown_x + 10, option_y + 5))


# Function to reset the game
def reset_game():
    global board, current_player, game_over
    board = np.zeros((ROWS, COLUMNS), dtype=int)
    current_player = PLAYER
    game_over = False


# Function to check if a move is valid
def is_valid_location(col):
    return board[0][col] == 0


# Function to get the next open row
def get_next_open_row(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            return row


# Function to check for a win
def winning_move(piece):
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    return False


# Main game loop
def main():
    global current_player, game_over, dropdown_active
    running = True

    while running:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if y < CELL_SIZE:  # Handle button clicks
                    if 10 <= x <= 130 and 10 <= y <= 50:  # New Game button
                        reset_game()
                    elif 10 <= x <= 130 and 60 <= y <= 100:  # Restart button
                        reset_game()
                    elif SCREEN_WIDTH - 120 <= x <= SCREEN_WIDTH - 40 and 20 <= y <= 60:  # Alpha-beta toggle
                        toggle_alpha_beta_pruning()
                    elif (SCREEN_WIDTH - 120) // 2 <= x <= (SCREEN_WIDTH - 120) // 2 + 120 and 20 <= y <= 60:  # Theme dropdown
                        dropdown_active = not dropdown_active
                    elif dropdown_active:  # Theme selection
                        for i, theme in enumerate(THEMES.keys()):
                            option_y = 60 + i * 40
                            if option_y <= y < option_y + 40:
                                apply_theme(theme)
                                dropdown_active = False
                                break
                elif not game_over and y > CELL_SIZE:  # Handle board clicks
                    col = x // CELL_SIZE
                    if is_valid_location(col):
                        row = get_next_open_row(col)
                        board[row][col] = current_player

                        if winning_move(current_player):
                            print(f"Player {current_player} wins!")
                            game_over = True

                        current_player = PLAYER if current_player == AI else AI

        pygame.display.update()


if __name__ == "__main__":
    main()
