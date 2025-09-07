import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600,800
COLOR_PICKER_HEIGHT = 600

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Color Picker")

# Function to generate a gradient
def draw_color_picker(surface, width, height):
    for y in range(height):
        for x in range(width):
            r = x * 255 // width
            g = y * 255 // height
            b = 255 - ((x + y) * 255 // (width + height))  # Dynamic blue component
            surface.set_at((x, y), (r, g, b))


# Main loop
def main():
    clock = pygame.time.Clock()
    selected_color = (0, 0, 0)
    color_picker_surface = pygame.Surface((WIDTH, COLOR_PICKER_HEIGHT))

    # Draw the color picker gradient
    draw_color_picker(color_picker_surface, WIDTH, COLOR_PICKER_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    if y < COLOR_PICKER_HEIGHT:
                        selected_color = color_picker_surface.get_at((x, y))

        # Draw everything
        screen.fill((255, 255, 255))
        screen.blit(color_picker_surface, (0, 0))
        pygame.draw.rect(screen, selected_color, (0, COLOR_PICKER_HEIGHT, WIDTH, HEIGHT - COLOR_PICKER_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
