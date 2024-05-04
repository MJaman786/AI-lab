from heapq import heappush, heappop
import numpy as np

class PuzzleState:
    def __init__(self, board, parent=None, action=None, depth=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = self.calculate_cost()

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def find_blank(self):
        return np.where(self.board == 0)

    def move(self, direction):
        blank_row, blank_col = self.find_blank()
        new_board = np.copy(self.board)

        if direction == 'up' and blank_row > 0:
            new_board[blank_row, blank_col], new_board[blank_row - 1, blank_col] = \
                new_board[blank_row - 1, blank_col], new_board[blank_row, blank_col]
            return PuzzleState(new_board, self, 'up', self.depth + 1)

        elif direction == 'down' and blank_row < 2:
            new_board[blank_row, blank_col], new_board[blank_row + 1, blank_col] = \
                new_board[blank_row + 1, blank_col], new_board[blank_row, blank_col]
            return PuzzleState(new_board, self, 'down', self.depth + 1)

        elif direction == 'left' and blank_col > 0:
            new_board[blank_row, blank_col], new_board[blank_row, blank_col - 1] = \
                new_board[blank_row, blank_col - 1], new_board[blank_row, blank_col]
            return PuzzleState(new_board, self, 'left', self.depth + 1)

        elif direction == 'right' and blank_col < 2:
            new_board[blank_row, blank_col], new_board[blank_row, blank_col + 1] = \
                new_board[blank_row, blank_col + 1], new_board[blank_row, blank_col]
            return PuzzleState(new_board, self, 'right', self.depth + 1)

        return None

    def calculate_cost(self):
        goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        cost = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    goal_position = np.where(goal_state == self.board[i][j])
                    cost += abs(i - goal_position[0][0]) + abs(j - goal_position[1][0])
        return cost

def a_star_search(initial_state):
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    if np.array_equal(initial_state.board, goal_state):
        return []

    pq = []
    heappush(pq, initial_state)
    visited = set()

    while pq:
        current_state = heappop(pq)
        visited.add(tuple(map(tuple, current_state.board)))
        #generating successor states
        for action in ['up', 'down', 'left', 'right']:
            next_state = current_state.move(action)
            if next_state and tuple(map(tuple, next_state.board)) not in visited:
                if np.array_equal(next_state.board, goal_state):
                    # Reconstruct the path
                    path = []
                    while next_state.parent:
                        path.append(next_state.action)
                        next_state = next_state.parent
                    return list(reversed(path))

                heappush(pq, next_state)

    return None

def main():
    initial_board = np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
    initial_state = PuzzleState(initial_board)
    solution = a_star_search(initial_state)

    if solution:
        print("Solution Path:")
        for move in solution:
            print(move)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
    
    
