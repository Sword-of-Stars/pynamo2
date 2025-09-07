import pygame
import functools
import importlib

from ...gui_elements.region import Region
from ...misc.core_functions import prep_image

class ImageBox(Region):
    '''
    A class representing a movable image box that contains multiple images and allows interaction

    Inherits from:
    --------------
    Region : A base class that defines a rectangular area.

    Methods:
    ---------
    __init__(config):
        Initializes the `ImageBox` object using the provided configuration. Loads the images, sets their initial positions, 
        and associates functions for interactions.
    
    set_rects():
        Calculates and sets the position and size (rectangles) of each image in the box.

    set_functions():
        Assigns functions to each image from a dynamically imported module based on the configuration. 
        The arguments for these functions are dynamically constructed using a recursive attribute getter.

    update_args():
        Updates the function arguments for each image based on the current object state. 
        Similar to `set_functions` but called before each function execution to ensure updated arguments.

    draw_images(pos, state, screen):
        Draws the images on the screen. Handles interaction such as checking if the mouse is over the image and 
        if the image is being clicked, calling the corresponding function if necessary.

    update(pos, state, rel, screen):
        Updates the `ImageBox` object by redrawing the box and images on the screen, and checking for any user interactions.
    '''

    def __init__(self, config):
        '''
        Initializes the ImageBox object.

        Parameters:
        -----------
        config : dict
            Configuration dictionary that includes the following keys:
                - 'rect': A tuple or list defining the rectangular area of the ImageBox.
                - 'images': A list of dictionaries, each containing:
                    - 'path': Path to the image file.
                    - 'scale': Scale factor for resizing the image.
                    - 'offset': (x, y) offset of the image from the top-left corner of the box.
                    - 'function': Name of a function to be called when the image is clicked.
                    - 'self_args': Attributes of the ImageBox to be passed as arguments to the function.
                    - 'args': Additional arguments for the function.
                - 'movable': Boolean indicating if the images should move slightly when hovered over.

        The constructor initializes the images, calculates their rects, and associates functions from the module.
        '''
        Region.__init__(self, *config['rect'])  # Initialize the base Region class with the rectangle.

        # Preprocess the images and set up their initial states
        self.images = [{'img': prep_image(pygame.image.load(i['path']), i['scale']), 
                        'is_active': False, **i} for i in config['images']]
        
        # Configurable option to allow movement on hover
        self.movable = config['movable']
        
        self.set_rects()    # Set the image rectangles.
        self.set_functions()  # Set the functions for each image.

    def set_rects(self):
        '''
        Sets the rectangular areas (rects) for each image based on their offsets and sizes.
        '''
        for img in self.images:
            rect = img['img'].get_rect()  # Get the rect (position and size) of the image.
            # Calculate the final position by adding the offset to the ImageBox position.
            img['rect'] = pygame.Rect(self.rect.x + img['offset'][0], 
                                      self.rect.y + img['offset'][1],
                                      rect[2], rect[3])

    def set_functions(self):
        '''
        Dynamically assigns functions to each image based on the configuration.

        If an image has a function, it is fetched from a module specified in "config.functions".
        Arguments for the function are built dynamically using recursive attribute fetching.
        '''
        def rgetattr(obj, attr, *args):
            '''
            Recursively fetches attributes from an object by following a dot-separated string path.
            '''
            def _getattr(obj, attr):
                return getattr(obj, attr, *args)
            return functools.reduce(_getattr, [obj] + attr.split('.'))
        
        self.args = []
        # Import the module containing the functions specified in the config.
        module = importlib.import_module("config.functions")  
        for img in self.images:
            if hasattr(module, img['function']):
                function = getattr(module, img['function'])  # Fetch the function dynamically.
                img['function'] = function

                # Build the arguments for the function using self attributes and other config values.
                args = [rgetattr(self, arg) for arg in img['self_args']]
                for i in img['args']:
                    args.append(i)
                img['use_args'] = args

            else:
                print(f"Function {img['function']} not found")  # Handle missing function.
                img['function'] = None

    def update_args(self):
        '''
        Updates the arguments for each image's function by re-fetching object attributes.
        This ensures that the arguments reflect the current state of the ImageBox.
        '''
        def rgetattr(obj, attr, *args):
            '''
            Recursively fetches attributes from an object by following a dot-separated string path.
            '''
            def _getattr(obj, attr):
                return getattr(obj, attr, *args)
            return functools.reduce(_getattr, [obj] + attr.split('.'))
        
        for img in self.images:
            # Update the arguments dynamically by fetching the latest values.
            args = [rgetattr(self, arg) for arg in img['self_args']]
            for i in img['args']:
                args.append(i)
            img['use_args'] = args

    def draw_images(self, pos, state, screen):
        '''
        Draws each image in the ImageBox on the screen, and handles interaction like hovering and clicking.

        Parameters:
        -----------
        pos : tuple
            The current mouse position (x, y).
        state : list
            Mouse button states. state[0] is True if the left mouse button is pressed.
        screen : pygame.Surface
            The screen surface where the images are drawn.
        '''
        for image in self.images:
            x, y = image['rect'].topleft  # Get the top-left position of the image.
            # Check if the mouse is hovering over the image.
            if image['rect'].collidepoint(pos):
                if self.movable:  # Move the image slightly if it's set as movable.
                    y -= 5
                if state[0] and not image['is_active']:  # Check if the image is clicked.
                    image['is_active'] = True
                    if image['function'] is not None:
                        self.update_args()  # Ensure the latest arguments are used.
                        image['function'](*image['use_args'])  # Call the function with the updated arguments.
                elif not state[0]:
                    image['is_active'] = False
            else:
                image['is_active'] = False
            
            # Draw the image on the screen at its current position.
            screen.blit(image['img'], (x, y))

    def update(self, pos, state, rel, screen):
        '''
        Updates the ImageBox by redrawing the images and handling interactions.

        Parameters:
        -----------
        pos : tuple
            Current mouse position (x, y).
        state : list
            Mouse button states.
        rel : tuple
            Mouse movement (dx, dy) (not used here but could be extended).
        screen : pygame.Surface
            The screen surface to draw on.
        '''
        self.draw(screen)  # Draw the background region (assumed to be in the parent class).
        self.draw_images(pos, state, screen)  # Draw the images and handle interaction.
