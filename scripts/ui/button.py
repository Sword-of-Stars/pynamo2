import pygame
import json

class Button():
    '''
    A basic button class for UI
    '''
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

        self.args = config["args"]


        self.layer = 0
        
        # Load sounds
        # self.hover_sound = pygame.mixer.Sound(self.hover_sound_path)
        # self.click_sound = pygame.mixer.Sound(self.click_sound_path)
        
        # Button state
        self.rect = pygame.Rect(self.position, self.size)
        self.is_hovered = False
        
        # Load font
        self.font = pygame.font.SysFont(None, self.font_size)

    def draw(self, camera):
        '''
        Draws the button to the camera display
        '''
        # Determine the color based on hover state
        color = self.hover_color if self.is_hovered else self.default_color
        
        # Draw button rectangle
        pygame.draw.rect(camera.display, color, self.rect)
        
        # Render the text
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        camera.display.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_click):
        '''
        Checks whether the button is hovered over
        or selected
        '''
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

# Function to load GUI elements from a JSON file
def load_buttons_from_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return [Button(x) for x in config['buttons']]