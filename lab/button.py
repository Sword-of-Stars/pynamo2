import pygame
import json

class Button:
    def __init__(self, config):
        # Initialize button properties from config
        self.position = config["position"]
        self.size = config["size"]
        self.default_color = config["default_color"]
        self.hover_color = config["hover_color"]
        self.text = config["text"]
        self.font_size = config["font_size"]
        self.font_color = config["font_color"]
        self.hover_sound_path = config["hover_sound"]
        self.click_sound_path = config["click_sound"]
        
        # Load sounds
        #self.hover_sound = pygame.mixer.Sound(self.hover_sound_path)
        #self.click_sound = pygame.mixer.Sound(self.click_sound_path)
        
        # Button state
        self.rect = pygame.Rect(self.position, self.size)
        self.is_hovered = False
        
        # Load font
        self.font = pygame.font.SysFont(None, self.font_size)

    def draw(self, screen):
        # Determine the color based on hover state
        color = self.hover_color if self.is_hovered else self.default_color
        
        # Draw button rectangle
        pygame.draw.rect(screen, color, self.rect)
        
        # Render the text
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_click):
        # Check if mouse is hovering over the button
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                pass
                #self.hover_sound.play()  # Play hover sound if first time hovered
            self.is_hovered = True
            
            if mouse_click:  # If mouse is clicked while hovering
                pass
                #self.click_sound.play()  # Play click sound
                return True  # Indicate button was clicked
        else:
            self.is_hovered = False
        
        return False  # Indicate no click

# Function to load button configuration from a JSON file
def load_button_from_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return Button(config['button'])

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Button Example')
clock = pygame.time.Clock()

# Load button from config
button = load_button_from_config('lab/config.json')

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0] # change to an event

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((255, 255, 255))
    
    # Update and draw the button
    if button.update(mouse_pos, mouse_click):
        print("Button clicked!")

    button.draw(screen)
    
    # Refresh the display
    pygame.display.flip()
    
    # Frame rate
    clock.tick(60)

# Clean up
pygame.quit()
