import tkinter as tk
import numpy as np
import random

class ConnectFourGUI:
    def __init__(self, root, max_depth=5, use_alpha_beta=True):
        self.root = root
        self.root.title("Connect Four")
        self.board = np.zeros((6, 7), int)
        self.max_depth = max_depth
        self.use_alpha_beta = use_alpha_beta
        self.current_player = 1  # Player 1 starts
        self.buttons = []
        self.labels = []
        self.create_widgets()

    def create_widgets(self):
        """Create the game grid and buttons."""
        # Create buttons for each column
        for col in range(7):
            button = tk.Button(self.root, text="↓", font=('Arial', 20), width=4, height=2, command=lambda col=col: self.drop_piece(col))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        # Create a grid for the board
        for row in range(6):
            label_row = []
            for col in range(7):
                label = tk.Label(self.root, text="", width=6, height=3, relief="solid", bg="lightblue")
                label.grid(row=row + 1, column=col)
                label_row.append(label)
            self.labels.append(label_row)

    def drop_piece(self, col):
        """Simulate dropping a piece for the current player in the given column."""
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.update_gui(row, col)
                if self.check_winner(row, col):
                    self.display_winner()
                    return
                self.current_player = 3 - self.current_player  # Switch player
                if self.current_player == 2:
                    self.ai_move()
                return

    def update_gui(self, row, col):
        """Update the GUI to reflect the current board state."""
        if self.board[row][col] == 1:
            color = "red"
        elif self.board[row][col] == 2:
            color = "yellow"
        self.labels[row][col].config(bg=color)

    def ai_move(self):
        """AI's move using the Minimax algorithm."""
        print("AI is thinking...")
        eval_score, best_move = self.minimax(self.max_depth, float('-inf'), float('inf'), True)
        print(f"AI chooses column {best_move}")
        self.drop_piece(best_move)

    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        valid_moves = self.get_valid_moves()
        if depth == 0 or not valid_moves:
            return self.evaluate_board(), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for col in valid_moves:
                row = self.simulate_move(col, 2)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(row, col)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for col in valid_moves:
                row = self.simulate_move(col, 1)
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(row, col)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_valid_moves(self):
        """Returns a list of valid column indices."""
        return [col for col in range(7) if self.board[0][col] == 0]

    def simulate_move(self, col, player):
        """Simulate a move without updating the GUI."""
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return row

    def undo_move(self, row, col):
        """Undo a simulated move."""
        self.board[row][col] = 0

    def evaluate_board(self):
        """Heuristic to evaluate the current board state."""
        return random.randint(-10, 10)  # A placeholder for your heuristic

    def check_winner(self, row, col):
        """Check if the current player has won after placing their piece."""
        # Check vertical, horizontal, and diagonal lines for a winner
        return self.check_line(row, col, 0, 1) or self.check_line(row, col, 1, 0) or self.check_line(row, col, 1, 1) or self.check_line(row, col, 1, -1)

    def check_line(self, row, col, d_row, d_col):
        """Check for a line of 4 pieces."""
        player = self.board[row][col]
        count = 1
        for i in range(1, 4):
            r, c = row + d_row * i, col + d_col * i
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 4):
            r, c = row - d_row * i, col - d_col * i
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
            else:
                break
        return count >= 4

    def display_winner(self):
        """Display the winner in the GUI."""
        winner = "Red (Player 1)" if self.current_player == 1 else "Yellow (Player 2)"
        winner_label = tk.Label(self.root, text=f"{winner} Wins!", font=('Arial', 20, 'bold'), fg="green")
        winner_label.grid(row=7, column=0, columnspan=7)

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFourGUI(root, max_depth=5, use_alpha_beta=True)
    root.mainloop()
