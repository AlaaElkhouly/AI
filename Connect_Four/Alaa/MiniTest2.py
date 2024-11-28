import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ROWS, COLS = 6, 7

# Core Connect Four functions
def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def is_valid_location(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

# Recursive plotting function to avoid intersection and overlapping
def plot_tree(ax, board, depth, maximizingPlayer, x, y, dx, dy):
    if depth == 0:
        ax.text(x, y-0.01, "(S)", ha="center", fontsize= 8, color="blue") # s for score at leaf node
        return

    valid_locations = get_valid_locations(board)
    num_children = len(valid_locations)

    for i, col in enumerate(valid_locations):
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 1 if maximizingPlayer else 2)

        # Calculate position for child nodes
        child_x = x - dx * (num_children - 1) / 2 + i * dx
        child_y = y - dy

        # Draw the connection and node
        ax.plot([x, child_x], [y, child_y], color="black", lw=0.2) # 0<lw<1 controls transarency of color the transparent=0
        ax.text(child_x, child_y, f"P{col}", ha="center", fontsize=8, color="black") # P {Should express the place on board}
        plot_tree(ax, temp_board, depth - 1, not maximizingPlayer, child_x, child_y, dx/2, dy)

# GUI for interactive tree display
def display_plot_gui():
    # Create a new tkinter window
    root = tk.Tk()
    root.title("Connect Four Decision Tree - Interactive")

    # Create a matplotlib figure
    fig = Figure(figsize=(10, 8)) # lama kabarto kan kwys takes up memory tho!!!!!!!!!!!!!!!!!!!!!
    ax = fig.add_subplot(111)
    ax.axis("off")  # Turn off axes

    # Initial plotting parameters
    board = create_board()
    depth = 3
    plot_tree(ax, board, depth=depth, maximizingPlayer=True, x=0.5, y=1.0, dx=0.02, dy=0.15)

    # Embed the matplotlib figure into tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Allow zooming and dragging via matplotlib's built-in tools
    toolbar = canvas.get_tk_widget()
    toolbar.pack()
    canvas.draw()

    # Add zoom and drag support using Matplotlib's toolbar
    toolbar_frame = tk.Frame(root)
    toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
    toolbar_button = FigureCanvasTkAgg(fig, master=toolbar_frame)
    toolbar_button.get_tk_widget().pack(side=tk.LEFT)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    display_plot_gui()
