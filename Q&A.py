import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Educational Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font setup
font = pygame.font.SysFont(None, 48)

# Questions and answers
questions = [
    {"question": "What is 2 + 2?", "answers": ["3", "4"], "correct": "4"},
    {"question": "What is the capital of France?", "answers": ["Paris", "London"], "correct": "Paris"},
    {"question": "What is the largest planet?", "answers": ["Jupiter", "Earth"], "correct": "Jupiter"},
]

# Function to display text
def display_text(text, color, x, y, font_size=48):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game function
def game():
    score = 0
    game_running = True

    while game_running:
        # Randomly pick a question
        question = random.choice(questions)
        question_text = question["question"]
        correct_answer = question["correct"]
        random.shuffle(question["answers"])
        answer_1 = question["answers"][0]
        answer_2 = question["answers"][1]

        # Set positions for the answers
        answer_1_pos = (100, 300)
        answer_2_pos = (100, 400)

        # Draw background
        screen.fill(WHITE)

        # Display question
        display_text(question_text, BLACK, 100, 100)

        # Display answers
        display_text(answer_1, GREEN if answer_1 == correct_answer else RED, *answer_1_pos)
        display_text(answer_2, GREEN if answer_2 == correct_answer else RED, *answer_2_pos)

        # Update the screen
        pygame.display.update()

        # Wait for the user to select an answer by mouse click
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    waiting_for_input = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the click is on the first answer
                    if answer_1_pos[0] <= mouse_x <= answer_1_pos[0] + 200 and answer_1_pos[1] <= mouse_y <= answer_1_pos[1] + 50:
                        if answer_1 == correct_answer:
                            score += 1
                        waiting_for_input = False
                    
                    # Check if the click is on the second answer
                    elif answer_2_pos[0] <= mouse_x <= answer_2_pos[0] + 200 and answer_2_pos[1] <= mouse_y <= answer_2_pos[1] + 50:
                        if answer_2 == correct_answer:
                            score += 1
                        waiting_for_input = False

        # Display score
        display_text(f"Score: {score}", BLACK, 300, 500, font_size=36)
        pygame.display.update()

        # Pause before the next question
        pygame.time.wait(1000)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game()
