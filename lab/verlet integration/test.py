import pygame
import numpy as np

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Parameters
num_particles_x = 20
num_particles_y = 20
spacing = 20
gravity = np.array([0, 0.5])
damping = 0.99

# Particle class
class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.prev_pos = np.array([x, y], dtype=float)
        self.acc = np.zeros(2)

    def update(self):
        velocity = (self.pos - self.prev_pos) * damping
        self.prev_pos = self.pos.copy()
        self.pos += velocity + self.acc
        self.acc = np.zeros(2)

    def apply_force(self, force):
        self.acc += force

# Create particles
particles = []
for i in range(num_particles_y):
    row = []
    for j in range(num_particles_x):
        row.append(Particle(j * spacing + 100, i * spacing + 100))
    particles.append(row)

# Constraints
constraints = []
for i in range(num_particles_y):
    for j in range(num_particles_x):
        if i < num_particles_y - 1:
            constraints.append((particles[i][j], particles[i + 1][j]))
        if j < num_particles_x - 1:
            constraints.append((particles[i][j], particles[i][j + 1]))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity
    for row in particles:
        for p in row:
            p.apply_force(gravity)

    # Update particles
    for row in particles:
        for p in row:
            p.update()

    # Satisfy constraints
    for _ in range(5):
        for p1, p2 in constraints:
            delta = p2.pos - p1.pos
            dist = np.linalg.norm(delta)
            if dist > 0:
                diff = (dist - spacing) / dist
                p1.pos += delta * 0.5 * diff
                p2.pos -= delta * 0.5 * diff

    # Render
    screen.fill((0, 0, 0))
    for p1, p2 in constraints:
        pygame.draw.line(screen, (255, 255, 255), p1.pos, p2.pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()