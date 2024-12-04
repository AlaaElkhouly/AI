"Tree Working Code"
"Please Copy it in an empty file to edit it"
"DO NOT EDIT HERE! (Please)"
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ROWS, COLS = 6, 7
layers=int(input("depth of gui tree?"))

# Connect Four core functions
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

# Generate decision tree as indented text
def generate_tree_text(board, depth, maximizingPlayer, level=0):
    if depth == 0:
        return f"{'    ' * level}└── [Leaf Node]\n"
    text = ""
    for i, col in enumerate(get_valid_locations(board)):
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 1 if maximizingPlayer else 2)
        connector = "└──" if i == len(get_valid_locations(board)) - 1 else "├──"
        text += f"{'    ' * level}{connector} Move: Column {col}\n"
        text += generate_tree_text(temp_board, depth-1, not maximizingPlayer, level+1)
    return text

# Plot tree graphically
def plot_tree(ax, board, depth, maximizingPlayer, x=0.5, y=1, dx=0.25):
    if depth == 0:
        ax.text(x, y-0.01, "(S)", ha="center", fontsize=8, color="green") #s for score
        return
    valid_locations = get_valid_locations(board)
    for i, col in enumerate(valid_locations):
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, 1 if maximizingPlayer else 2)
        child_x = x - dx + i * (2 * dx / (len(valid_locations) - 1 if len(valid_locations) > 1 else 1))
        child_y = y - 0.1
        ax.plot([x, child_x], [y, child_y], color="black", lw=0.15)
        ax.text(child_x, child_y, f"P{col}", ha="center", fontsize=8) #p{col} should describe the point on board
        plot_tree(ax, temp_board, depth-1, not maximizingPlayer, child_x, child_y, dx * 0.5)

# GUI for text-based decision tree
def display_tree_gui(layers):
    root = tk.Tk()
    root.title("Connect Four Decision Tree - Text")
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar.set)
    text_box.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_box.yview)
    board = create_board()
    tree_text = generate_tree_text(board, layers , maximizingPlayer=True)
    text_box.insert(tk.END, tree_text)
    root.mainloop()

# GUI for graphical decision tree
def display_plot_gui(layers):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("off")
    board = create_board()
    plot_tree(ax, board, layers, maximizingPlayer=True)
    root = tk.Tk()
    root.title("Connect Four Decision Tree - Plot")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
    root.mainloop()

# Run both GUIs
if __name__ == "__main__":
    # Uncomment one of the following lines to view its GUI
    display_tree_gui(layers)
    #display_plot_gui(layers)

