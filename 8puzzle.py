import pygame
import sys
import random
from queue import PriorityQueue
from collections import deque

# Constants
GRID_SIZE = 3
TILE_SIZE = 100
MARGIN = 2
SCREEN_SIZE = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
FONT_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Utility function to create a shuffled puzzle with numbers 1-8 and an empty space
def create_puzzle():
    tiles = list(range(1, GRID_SIZE**2)) + [None]
    random.shuffle(tiles)
    
    puzzle = [tiles[i:i + GRID_SIZE] for i in range(0, len(tiles), GRID_SIZE)]
    return puzzle

# Utility function to find the coordinates of the empty space in the puzzle
def find_empty(puzzle):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] is None:
                return (i, j)
    return None

# Function to display the puzzle on the Pygame screen
def draw_puzzle(screen, puzzle, font):
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * TILE_SIZE + (j + 1) * MARGIN
            y = i * TILE_SIZE + (i + 1) * MARGIN
            value = puzzle[i][j]
            if value is not None:
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                text = font.render(str(value), True, WHITE)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.display.flip()

# Function to move a tile into the empty space
def move_tile(puzzle, direction):
    empty_x, empty_y = find_empty(puzzle)
    new_x, new_y = empty_x, empty_y

    if direction == 'up':
        new_x -= 1
    elif direction == 'down':
        new_x += 1
    elif direction == 'left':
        new_y -= 1
    elif direction == 'right':
        new_y += 1

    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        puzzle[empty_x][empty_y], puzzle[new_x][new_y] = puzzle[new_x][new_y], puzzle[empty_x][empty_y]
        return True
    return False

# Heuristic for A* - Manhattan distance
def manhattan_distance(puzzle, goal):
    distance = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = puzzle[i][j]
            if value is not None:
                goal_pos = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if goal[x][y] == value][0]
                distance += abs(goal_pos[0] - i) + abs(goal_pos[1] - j)
    return distance

# A* Solver for 8-puzzle
def solve_puzzle(start_puzzle, goal_puzzle):
    initial_state = (manhattan_distance(start_puzzle, goal_puzzle), 0, start_puzzle, [])
    open_list = PriorityQueue()
    open_list.put(initial_state)
    closed_list = set()

    while not open_list.empty():
        _, level, current_puzzle, path = open_list.get()
        if current_puzzle == goal_puzzle:
            return path

        closed_list.add(tuple(map(tuple, current_puzzle)))

        empty_x, empty_y = find_empty(current_puzzle)

        # Ensure new_x and new_y are initialized properly
        for direction, (dx, dy) in zip(['up', 'down', 'left', 'right'], [(-1, 0), (1, 0), (0, -1), (0, 1)]):
            new_x = empty_x + dx  # Initialize new_x
            new_y = empty_y + dy  # Initialize new_y

            # Ensure new_x and new_y are within bounds before proceeding
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                new_puzzle = [row[:] for row in current_puzzle]  # Deep copy
                new_puzzle[empty_x][empty_y], new_puzzle[new_x][new_y] = (
                    new_puzzle[new_x][new_y],
                    new_puzzle[empty_x][empty_y],
                )

                if tuple(map(tuple, new_puzzle)) not in closed_list:
                    new_level = level + 1
                    h = manhattan_distance(new_puzzle, goal_puzzle)
                    open_list.put((new_level + h, new_level, new_puzzle, path + [direction]))
    return []


# Main game loop with Pygame
def play():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("8-Puzzle")
    font = pygame.font.Font(None, FONT_SIZE)

    # Define the goal puzzle for 8-puzzle
    goal_puzzle = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, None]
    ]

    puzzle = create_puzzle()
    while puzzle == goal_puzzle:  # Ensure it's not solved at start
        puzzle = create_puzzle()

    draw_puzzle(screen, puzzle, font)

    solved_path = deque()
    is_auto_solving = False
    solved_path = deque(solve_puzzle(puzzle, goal_puzzle))  # Get the solving path with A* and store it

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset the puzzle
                    puzzle = create_puzzle()
                    solved_path = deque(solve_puzzle(puzzle, goal_puzzle))
                    draw_puzzle(screen, puzzle, font)
                elif event.key == pygame.K_s:  # Toggle automatic solving
                    is_auto_solving = not is_auto_solving
                elif not is_auto_solving:
                    if event.key == pygame.K_UP:
                        if move_tile(puzzle, 'down'):
                            draw_puzzle(screen, puzzle, font)
                    elif event.key == pygame.K_DOWN:
                        if move_tile(puzzle, 'up'):
                            draw_puzzle(screen, puzzle, font)
                    elif event.key == pygame.K_LEFT:
                        if move_tile(puzzle, 'right'):
                            draw_puzzle(screen, puzzle, font)
                    elif event.key == pygame.K_RIGHT:
                        if move_tile(puzzle, 'left'):
                            draw_puzzle(screen, puzzle, font)

        if is_auto_solving and solved_path:
            move = solved_path.popleft()  # Get the next move from the solving path
            move_tile(puzzle, move)  # Apply the move
            draw_puzzle(screen, puzzle, font)  # Redraw the puzzle
            pygame.time.delay(200)  # Small delay for smoother animation

        if not solved_path:  # When the puzzle is solved
            font = pygame.font.Font(None, 50)
            text = font.render("Puzzle Solved!", True, GREEN)
            # text_rect isTextured to be able to 


play()