import pygame

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Define the paddles and ball
left_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball movement speed
ball_speed_x = 5
ball_speed_y = 5

# Paddle movement speed
paddle_speed = 6

# Scores
left_score = 0
right_score = 0

# Font for score display
font = pygame.font.SysFont("Arial", 30)

def display_score():
    global left_score, right_score
    score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

def main():
    global ball_speed_x, ball_speed_y, left_score, right_score
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:  # Move left paddle up
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:  # Move left paddle down
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:  # Move right paddle up
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:  # Move right paddle down
            right_paddle.y += paddle_speed

        # Ball movement and collision with walls
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x = -ball_speed_x

        # Scoring logic
        if ball.left <= 0:
            right_score += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = -ball_speed_x  # Reset ball to move towards the opponent
        if ball.right >= SCREEN_WIDTH:
            left_score += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = -ball_speed_x  # Reset ball to move towards the opponent

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Display score
        display_score()

        # Update the screen
        pygame.display.update()

        # Control the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
