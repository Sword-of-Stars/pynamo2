import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer with Grappling Hook")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 20
player_color = BLUE
player_pos = [100, 500]
player_vel = [0, 0]
player_speed = 5
gravity = 0.5
jump_strength = -10

# Grappling hook settings
hook_length = 200
hook_attached = False
hook_pos = None

# Platforms
platforms = [
    pygame.Rect(50, 550, 700, 20),
    pygame.Rect(200, 400, 100, 20),
    pygame.Rect(400, 300, 100, 20),
    pygame.Rect(600, 200, 100, 20)
]

def draw_player():
    pygame.draw.rect(screen, player_color, (*player_pos, player_size, player_size))

def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

def draw_hook():
    if hook_attached and hook_pos:
        pygame.draw.line(screen, RED, (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2), hook_pos, 2)

def handle_movement(keys):
    if keys[pygame.K_LEFT]:
        player_vel[0] = -player_speed
    elif keys[pygame.K_RIGHT]:
        player_vel[0] = player_speed
    else:
        player_vel[0] = 0

    if keys[pygame.K_SPACE] and is_on_ground():
        player_vel[1] = jump_strength

def is_on_ground():
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_rect.bottom <= platform.bottom:
            return True
    return False

def update_player():
    global hook_attached, hook_pos

    if hook_attached and hook_pos:
        dx = hook_pos[0] - (player_pos[0] + player_size // 2)
        dy = hook_pos[1] - (player_pos[1] + player_size // 2)
        distance = math.sqrt(dx**2 + dy**2)
        if distance > hook_length:
            angle = math.atan2(dy, dx)
            player_pos[0] = hook_pos[0] - hook_length * math.cos(angle) - player_size // 2
            player_pos[1] = hook_pos[1] - hook_length * math.sin(angle) - player_size // 2
        else:
            hook_attached = False
            hook_pos = None

    player_vel[1] += gravity
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]

    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_vel[1] > 0:
                player_pos[1] = platform.top - player_size
                player_vel[1] = 0
            elif player_vel[1] < 0:
                player_pos[1] = platform.bottom
                player_vel[1] = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hook_pos = event.pos
            hook_attached = True

    keys = pygame.key.get_pressed()
    handle_movement(keys)
    update_player()

    screen.fill(WHITE)
    draw_platforms()
    draw_player()
    draw_hook()
    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()