import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Half-Circle Selection Wheel")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
HIGHLIGHT = (255, 100, 100)

# Number of sectors
NUM_SECTORS = 3
RADIUS = 200
CENTER = (WIDTH // 2, HEIGHT // 2)

# Function to draw a sector
def draw_sector(surface, color, center, radius, start_angle, end_angle):
    points = [center]
    for angle in range(start_angle, end_angle + 1):
        x = center[0] + int(radius * math.cos(math.radians(angle)))
        y = center[1] + int(radius * math.sin(math.radians(angle)))
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos
    dx = mouse_x - CENTER[0]
    dy = mouse_y - CENTER[1]
    mouse_angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

    # Draw sectors
    for i in range(NUM_SECTORS):
        start_angle = 180 + (i * 180 // NUM_SECTORS)
        end_angle = 180 + ((i + 1) * 180 // NUM_SECTORS)
        if start_angle <= mouse_angle < end_angle:
            color = HIGHLIGHT
        else:
            color = RED
        draw_sector(screen, color, CENTER, RADIUS, start_angle, end_angle)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()