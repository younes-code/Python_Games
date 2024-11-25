import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Define the player, bullets, and enemies
player = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
bullets = []
enemies = []

# Movement speed
player_speed = 5
bullet_speed = 7
enemy_speed = 2

# Score
score = 0

# Font for score and game over message
font = pygame.font.SysFont("Arial", 30)

def draw_player():
    pygame.draw.rect(screen, WHITE, player)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

def move_bullets():
    global score
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)  # Remove bullets that are off-screen

        for enemy in enemies[:]:
            if bullet.colliderect(enemy):  # Check for collision with enemies
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10  # Increase score when enemy is hit
                break

def move_enemies():
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top >= SCREEN_HEIGHT:  # If an enemy goes off the screen
            enemies.remove(enemy)

def spawn_enemy():
    if random.random() < 0.02:  # 2% chance to spawn an enemy each frame
        x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy = pygame.Rect(x, 0, ENEMY_WIDTH, ENEMY_HEIGHT)
        enemies.append(enemy)

def check_game_over():
    for enemy in enemies:
        if enemy.colliderect(player):  # Check if any enemy touches the player
            return True
    return False

def main():
    global score
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot bullet
                    bullet = pygame.Rect(player.centerx - BULLET_WIDTH // 2, player.top, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet)

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += player_speed

        # Move bullets and enemies
        move_bullets()
        move_enemies()

        # Spawn new enemies
        spawn_enemy()

        # Check if game over
        if check_game_over():
            draw_game_over()
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            running = False  # Stop the game loop

        # Draw the player, bullets, enemies, and score
        draw_player()
        draw_bullets()
        draw_enemies()
        draw_score()

        # Update the screen
        pygame.display.update()

        # Control the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
