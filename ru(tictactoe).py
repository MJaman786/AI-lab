def print_board(board):
    """Prints the Tic Tac Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    """Checks if there's a winner or if the game is a tie."""
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    # Check for tie
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        return "Tie"
    return None

def get_empty_cells(board):
    """Returns a list of empty cells (row, col) on the board."""
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_cells.append((i, j))
    return empty_cells

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to determine the best move for the AI player."""
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for cell in get_empty_cells(board):
            board[cell[0]][cell[1]] = "O"
            score = minimax(board, depth + 1, False)
            board[cell[0]][cell[1]] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for cell in get_empty_cells(board):
            board[cell[0]][cell[1]] = "X"
            score = minimax(board, depth + 1, True)
            board[cell[0]][cell[1]] = " "
            best_score = min(best_score, score)
        return best_score

def get_best_move(board):
    """Returns the best move for the AI player using the minimax algorithm."""
    best_move = None
    best_score = -float("inf")
    for cell in get_empty_cells(board):
        board[cell[0]][cell[1]] = "O"
        score = minimax(board, 0, False)
        board[cell[0]][cell[1]] = " "
        if score > best_score:
            best_score = score
            best_move = cell
    return best_move

def play_game():
    """Main function to play Tic Tac Toe with an AI player."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        # Print current board
        print("\nCurrent board:")
        print_board(board)

        if current_player == "X":
            # Human player's turn
            while True:
                row = int(input(f"Player {current_player}, enter row (0-2): "))
                col = int(input(f"Player {current_player}, enter column (0-2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                    board[row][col] = current_player
                    break
                else:
                    print("Invalid move. Try again.")
        else:
            # AI player's turn
            print("AI player (O) is making a move...")
            ai_row, ai_col = get_best_move(board)
            board[ai_row][ai_col] = "O"

        # Check for winner or tie
        winner = check_winner(board)
        if winner is not None:
            print("\nFinal board:")
            print_board(board)
            if winner == "Tie":
                print("It's a tie!")
            else:
                print(f"Player {winner} wins!")
            break

        # Switch player
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    play_game()
