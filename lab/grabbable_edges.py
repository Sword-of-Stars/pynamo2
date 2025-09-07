import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Accessible Edges of Rectangles")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define rectangles (x, y, width, height)
rectangles = [
    pygame.Rect(100, 100, 200, 150),
    pygame.Rect(150, 200, 250, 100),
    pygame.Rect(200, 400, 300, 150)
]

def draw_rectangles_and_edges():
    window.fill(WHITE)
    
    for rect in rectangles:
        pygame.draw.rect(window, BLACK, rect, 2)
        
        # Check and draw accessible edges
        for edge in get_accessible_edges(rect):
            pygame.draw.line(window, GREEN, edge[0], edge[1], 2)
    
    pygame.display.flip()

def get_accessible_edges(rect):
    edges = [
        ((rect.left, rect.top), (rect.right, rect.top)),  # Top edge
        ((rect.right, rect.top), (rect.right, rect.bottom)),  # Right edge
        ((rect.right, rect.bottom), (rect.left, rect.bottom)),  # Bottom edge
        ((rect.left, rect.bottom), (rect.left, rect.top))  # Left edge
    ]
    
    accessible_edges = []
    
    for edge in edges:
        if is_edge_accessible(edge):
            accessible_edges.append(edge)
    
    return accessible_edges

def is_edge_accessible(edge):
    for rect in rectangles:
        if rect.collidepoint(edge[0]) and rect.collidepoint(edge[1]):
            return False
    return True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_rectangles_and_edges()

pygame.quit()
sys.exit()