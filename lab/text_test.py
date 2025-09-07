import pygame
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font settings
FONT_SIZE = 24
FONT = pygame.font.Font(None, FONT_SIZE)

# Text box dimensions and position
TEXT_BOX_WIDTH = 600
TEXT_BOX_HEIGHT = 200
TEXT_BOX_X = (SCREEN_WIDTH - TEXT_BOX_WIDTH) // 2
TEXT_BOX_Y = (SCREEN_HEIGHT - TEXT_BOX_HEIGHT) // 2

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text Box Example")

def draw_text_box(displayed_text):
    """Draw the text box and the currently displayed text."""
    # Draw the text box background
    pygame.draw.rect(screen, WHITE, (TEXT_BOX_X, TEXT_BOX_Y, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT))
    pygame.draw.rect(screen, BLACK, (TEXT_BOX_X, TEXT_BOX_Y, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT), 2)

    # Draw the text
    lines = displayed_text.split("\n")
    for i, line in enumerate(lines):
        text_surface = FONT.render(line, True, BLACK)
        screen.blit(text_surface, (TEXT_BOX_X + 10, TEXT_BOX_Y + 10 + i * (FONT_SIZE + 5)))

def main():
    # Example text
    text = """This is the first line of text.
Here comes the second line.
And this is the third line.
Finally, the last line appears."""

    # Variables to track displayed text
    displayed_text = ""
    current_index = 0

    # Game loop variables
    running = True
    clock = pygame.time.Clock()

    # Delay between characters
    delay = 0.05  # Seconds
    last_update_time = time.time()

    while running:
        screen.fill(BLACK)  # Clear screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update displayed text
        if current_index < len(text) and time.time() - last_update_time >= delay:
            displayed_text += text[current_index]
            current_index += 1
            last_update_time = time.time()

        # Draw the text box
        draw_text_box(displayed_text)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
