def minimax(self, depth, alpha, beta, maximizing_player, parent_node=None):
    if depth == 0 or not self.get_valid_moves():
        score = self.evaluate_board()
        # Attach leaf node with score
        Node(f"Leaf: {score}", parent=parent_node)
        return score, None

    valid_moves = self.get_valid_moves()
    best_move = None

    if maximizing_player:
        max_value = -math.inf
        for column in valid_moves:
            self.player1_board = self.drop_piece(self.player1_board, column)
            
            # Create child node
            child_node = Node(f"Move: {column} (Max)", parent=parent_node)
            
            value, _ = self.minimax(depth - 1, alpha, beta, False, child_node)
            self.player1_board = self.undo_drop_piece(self.player1_board, column)

            if value > max_value:
                max_value = value
                best_move = column

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return max_value, best_move
    else:
        min_value = math.inf
        for column in valid_moves:
            self.player2_board = self.drop_piece(self.player2_board, column)

            # Create child node
            child_node = Node(f"Move: {column} (Min)", parent=parent_node)

            value, _ = self.minimax(depth - 1, alpha, beta, True, child_node)
            self.player2_board = self.undo_drop_piece(self.player2_board, column)

            if value < min_value:
                min_value = value
                best_move = column

            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_value, best_move
def display_tree(self):
    for pre, fill, node in RenderTree(self.tree_root):
        print(f"{pre}{node.name}")
def computer_turn(self):
    print("AI is thinking...")
    self.tree_root = Node("Root")  # Reset the tree for this turn
    _, move = self.minimax(self.max_depth, float('-inf'), float('inf'), True, self.tree_root)
    print(f"AI chooses column {move}")
    self.player1_board = self.drop_piece(self.player1_board, move)
    self.display_tree()  # Display the tree after the AI move
