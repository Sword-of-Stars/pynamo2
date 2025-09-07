
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line-Rectangle Collision Detection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Define a rectangle
    rect = pygame.Rect(300, 200, 200, 100)
    pygame.draw.rect(screen, BLACK, rect, 2)

    # Define a line
    line_start = (100, 100)
    line_end = pygame.mouse.get_pos()
    pygame.draw.line(screen, RED, line_start, line_end, 2)

    # Check for collision
    if rect.clipline(line_start, line_end):
        pygame.draw.rect(screen, RED, rect, 2)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
