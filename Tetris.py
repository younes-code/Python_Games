import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    'I': (255, 0, 0),
    'O': (0, 255, 0),
    'T': (0, 0, 255),
    'S': (255, 255, 0),
    'Z': (255, 165, 0),
    'L': (0, 255, 255),
    'J': (255, 0, 255),
}

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define the shapes and their labels
SHAPES = [
    ('I', [[(1, 1, 1, 1)]]),  # I-shape
    ('O', [[(1, 1), (1, 1)]]),  # O-shape
    ('T', [[(0, 1, 0), (1, 1, 1)]]),  # T-shape
    ('S', [[(1, 1, 0), (0, 1, 1)]]),  # S-shape
    ('Z', [[(0, 1, 1), (1, 1, 0)]]),  # Z-shape
    ('L', [[(1, 0, 0), (1, 1, 1)]]),  # L-shape
    ('J', [[(0, 0, 1), (1, 1, 1)]])   # J-shape
]

# Rotation function
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def draw_shape(shape, x, y):
    shape_label = shape[0]  # Get the shape label (e.g., 'I', 'O', etc.)
    shape_matrix = shape[1]  # Get the actual matrix representation of the shape
    color = COLORS[shape_label]  # Get the color for this shape

    for row_idx, row in enumerate(shape_matrix):
        for col_idx, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, color, (x + col_idx * BLOCK_SIZE, y + row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(grid, shape, x, y):
    shape_label = shape[0]
    shape_matrix = shape[1]
    for row_idx, row in enumerate(shape_matrix):
        for col_idx, val in enumerate(row):
            if val:
                if x + col_idx < 0 or x + col_idx >= SCREEN_WIDTH // BLOCK_SIZE or y + row_idx >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if y + row_idx >= len(grid) or grid[y + row_idx][x + col_idx]:
                    return True
    return False

def clear_lines(grid):
    new_grid = [row for row in grid if any(col == 0 for col in row)]
    lines_cleared = len(grid) - len(new_grid)
    new_grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(lines_cleared)] + new_grid
    return new_grid, lines_cleared

def main():
    # Set up game variables
    clock = pygame.time.Clock()
    grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    current_shape = random.choice(SHAPES)
    current_x, current_y = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[1][0]) // 2, 0
    running = True
    score = 0

    # Fall speed for the shape (the higher the value, the slower the fall)
    fall_speed = 10  # This will control how fast the piece falls (lower = faster fall)
    fall_count = 0  # Track the fall time

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the shape with arrow keys (left, right, rotate)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not check_collision(grid, current_shape, current_x - 1, current_y):
                current_x -= 1
        if keys[pygame.K_RIGHT]:
            if not check_collision(grid, current_shape, current_x + 1, current_y):
                current_x += 1
        if keys[pygame.K_UP]:
            rotated_shape = rotate_shape(current_shape[1])
            if not check_collision(grid, (current_shape[0], rotated_shape), current_x, current_y):
                current_shape = (current_shape[0], rotated_shape)

        # Handle automatic fall of the shape based on fall_speed
        fall_count += 1
        if fall_count >= fall_speed:
            if not check_collision(grid, current_shape, current_x, current_y + 1):
                current_y += 1
            else:
                # Place the shape on the grid and get a new one
                for row_idx, row in enumerate(current_shape[1]):
                    for col_idx, val in enumerate(row):
                        if val:
                            grid[current_y + row_idx][current_x + col_idx] = 1
                grid, cleared_lines = clear_lines(grid)
                score += cleared_lines
                current_shape = random.choice(SHAPES)
                current_x, current_y = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[1][0]) // 2, 0
                if check_collision(grid, current_shape, current_x, current_y):
                    running = False  # Game over

            fall_count = 0  # Reset the fall count

        # Draw the grid and the falling shape
        for y_idx, row in enumerate(grid):
            for x_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (x_idx * BLOCK_SIZE, y_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        draw_shape(current_shape, current_x * BLOCK_SIZE, current_y * BLOCK_SIZE)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(30)

    # Display game over
    pygame.quit()

if __name__ == "__main__":
    main()
