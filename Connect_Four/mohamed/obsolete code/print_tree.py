def save_and_encode_tree(player1_bitboard, player2_bitboard, queue):
    # Combine the bitboards into one and save to the queue
    combined_board = (player2_bitboard << 1) | player1_bitboard
    queue.append(combined_board)

def decode_and_print_tree(queue, rows=6, cols=7):
    # Iterate through each node in the queue
    for node_index, combined_board in enumerate(queue):
        print(f"Node {node_index}:")
        
        # Create an empty board to display
        board = [['.' for _ in range(cols)] for _ in range(rows)]
        
        # Decode the bitboard into the board representation
        for col in range(cols):
            for row in range(rows):
                bit_position = (col * rows) + row
                # Extract the two bits for the current cell
                cell_value = (combined_board >> (bit_position * 2)) & 0b11

                # Map the cell value to the appropriate symbol
                if cell_value == 0b01:  # Player 1
                    board[row][col] = 'X'
                elif cell_value == 0b10:  # Player 2
                    board[row][col] = 'O'

        # Print the board (flip vertically so the bottom row is printed last)
        for row in reversed(board):
            print(' '.join(row))
        print()  # Add a blank line between boards

# Example usage
queue = []

# Simulating a couple of board states
p1_board_1 = 0b000001000010000001000010000001000010
p2_board_1 = 0b000010000100000010000100000010000100
save_and_encode_tree(p1_board_1, p2_board_1, queue)

p1_board_2 = 0b000000000010000001000010000001000010
p2_board_2 = 0b000010000100000010000100000010000000
save_and_encode_tree(p1_board_2, p2_board_2, queue)

# Decode and print the boards in the queue
decode_and_print_tree(queue)
