import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
ROWS = 6
COLUMNS = 7
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 10

# Colors for the theme
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

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
pygame.display.set_caption("Connect Four :)")

# Font setup
font = pygame.font.Font(None, 36)

# Board and game state
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = 1
alpha_beta_pruning = False
dropdown_active = False

def draw_board():
    screen.fill((255, 255, 255))  # White background
    for row in range(ROWS):
        for col in range(COLUMNS):
            # Draw the 3D board background
            pygame.draw.rect(screen, BACKGROUND_COLOR, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, (0, 0, 0), (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), RADIUS + 5)

            # Draw the 3D effect of each piece
            if board[row][col] == 0:
                color = EMPTY_COLOR
            elif board[row][col] == 1:
                color = PLAYER_ONE_COLOR
            else:
                color = PLAYER_TWO_COLOR
            
            pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), RADIUS)

def toggle_alpha_beta_pruning():
    global alpha_beta_pruning
    alpha_beta_pruning = not alpha_beta_pruning

def draw_toggle_button():
    x, y, width, height = SCREEN_WIDTH - 120, 20, 80, 40
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=20)
    if alpha_beta_pruning:
        pygame.draw.circle(screen, (0, 255, 0), (x + width - height // 2, y + height // 2), height // 2 - 5)
    else:
        pygame.draw.circle(screen, (255, 0, 0), (x + height // 2, y + height // 2), height // 2 - 5)

    # Draw the label next to the toggle
    label = font.render("Alpha-Beta Pruning", True, (0, 0, 0))
    screen.blit(label, (x - 180, y + 5))

def draw_theme_dropdown():
    # Draw the dropdown button at the middle top of the screen but moved slightly to the left
    dropdown_x, dropdown_y, dropdown_w, dropdown_h = (SCREEN_WIDTH - 120) // 2 - 20, 20, 120, 40
    pygame.draw.rect(screen, (200, 200, 200), (dropdown_x, dropdown_y, dropdown_w, dropdown_h), border_radius=10)
    label = font.render("Theme", True, (0, 0, 0))
    screen.blit(label, (dropdown_x + 10, dropdown_y + 5))

    # If dropdown is active, show the theme options
    if dropdown_active:
        for i, theme in enumerate(THEMES.keys()):
            option_y = dropdown_y + dropdown_h + i * dropdown_h
            pygame.draw.rect(screen, (240, 240, 240), (dropdown_x, option_y, dropdown_w, dropdown_h), border_radius=10)
            option_text = font.render(theme, True, (0, 0, 0))
            screen.blit(option_text, (dropdown_x + 10, option_y + 5))

def apply_theme(theme_name):
    global BACKGROUND_COLOR, PLAYER_ONE_COLOR, PLAYER_TWO_COLOR, current_theme
    current_theme = theme_name
    theme = THEMES[theme_name]
    BACKGROUND_COLOR = theme["bg"]
    PLAYER_ONE_COLOR = theme["player1"]
    PLAYER_TWO_COLOR = theme["player2"]

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

def reset_game():
    global board, current_player
    board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = 1

# Main loop
running = True
while running:
    draw_board()
    draw_toggle_button()
    draw_theme_dropdown()
    
    # Draw New Game and Restart buttons at the top left corner, with wider buttons
    button_width, button_height = 120, 40  # Increased width, same height
    draw_button("New Game", 10, 10, button_width, button_height, (100, 200, 100))
    draw_button("Restart", 10, 60, button_width, button_height, (200, 100, 100))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            # Check for click on New Game button (top-left corner)
            if 10 <= x <= 130 and 10 <= y <= 50:
                reset_game()
            
            # Check for click on Restart button (top-left corner)
            elif 10 <= x <= 130 and 60 <= y <= 100:
                reset_game()
            
            # Check for click on toggle switch
            elif SCREEN_WIDTH - 120 <= x <= SCREEN_WIDTH - 40 and 20 <= y <= 60:
                toggle_alpha_beta_pruning()
            
            # Check for click on dropdown menu
            elif (SCREEN_WIDTH - 120) // 2 - 20 <= x <= (SCREEN_WIDTH - 120) // 2 + 100 and 20 <= y <= 60:
                dropdown_active = not dropdown_active  # Toggle dropdown menu
                
            # Check for theme selection if dropdown is active
            elif dropdown_active and (SCREEN_WIDTH - 120) // 2 - 20 <= x <= (SCREEN_WIDTH - 120) // 2 + 100:
                for i, theme_name in enumerate(THEMES.keys()):
                    option_y = 60 + i * 40
                    if option_y <= y < option_y + 40:
                        apply_theme(theme_name)
                        dropdown_active = False
                        break

            # Handle board clicks for placing pieces
            elif y > 60 and y < SCREEN_HEIGHT:
                col = x // CELL_SIZE
                for row in range(ROWS - 1, -1, -1):
                    if board[row][col] == 0:
                        board[row][col] = current_player
                        current_player = 1 if current_player == 2 else 2
                        break

    pygame.display.update()
