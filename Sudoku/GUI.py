#set of variables places 1-81
#domain list of possible values to fill variables with [1-9]
#constraints rules that do not allow you to assign some of the values to the variables
#_____________________Fills the board____________________________#
'''empty_board = '0' * 81
index=int("5")
num="7"
empty_board = empty_board[:index] + num + empty_board[index + 1:]
print(empty_board)'''
#_________________________GUI____________________________________#
import tkinter as tk

def toggle_mode():
    """Toggle between 'Mode 1' and 'Mode 2'."""
    if mode_button.config('text')[-1] == "Mode 1":
        mode_button.config(text="Mode 2")
    else:
        mode_button.config(text="Mode 1")

def restart():
    for i in range(9):
        for j in range(9):
            grid_entries[i][j].delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Sudoku GUI")
root.geometry("600x650")

# Create a frame for the Sudoku grid
grid_frame = tk.Frame(root, bg="white", bd=5)
grid_frame.pack(pady=5)

# Create a 9x9 grid of entry widgets
grid_entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        # Add thicker borders to divide 3x3 grids visually
        border_top = 6 if i % 3 == 0 else 1
        border_left = 6 if j % 3 == 0 else 1
        border_bottom = 6 if i == 8 else 1
        border_right = 6 if j == 8 else 1

        entry = tk.Entry(
            grid_frame,
            width=2,
            font=('Arial', 18),
            justify='center',
            bg="white",
            relief="solid",
            bd=1
        )
        entry.grid(
            row=i,
            column=j,
            padx=(0 if j == 0 else 2),
            pady=(0 if i == 0 else 2),
            ipadx=5,
            ipady=5,
            sticky='nsew'
        )
        entry.config(highlightbackground="black", highlightcolor="black")
        entry.grid(padx=(border_left, border_right), pady=(border_top, border_bottom))
        row_entries.append(entry)
    grid_entries.append(row_entries)
    def solve():
        return 0
# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

mode_button = tk.Button(button_frame, text="Mode 1", command=toggle_mode, width=10, font=('Arial', 14))
mode_button.pack(side=tk.LEFT, padx=20)

restart_button = tk.Button(button_frame, text="Restart", command=restart, width=10, font=('Arial', 14))
restart_button.pack(side=tk.LEFT, padx=20)

solve_button = tk.Button(button_frame, text="Solve", command=solve, width=10, font=('Arial', 14))
solve_button.pack(side=tk.RIGHT, padx=20)

# Add a label for Sudoku title
title_label = tk.Label(root, text="Sudoku Puzzle", font=('Arial', 20, 'bold'))
title_label.pack(pady=5)

root.mainloop()
#_________________________________________________________________##_________________________________________________________________#
