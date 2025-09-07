import pygame
from ...gui_elements.region import Region
from ...gui_elements.elements import Selectable, BuilderObject

class TriggerBox(Region):
    """
    TriggerBox is a UI component for managing and rendering trigger-related elements on a game screen. 
    It allows users to draw a trigger symbol, manage input text, and select or deselect trigger objects.

    Attributes:
    -----------
    offset : list
        Offset position for the trigger box rendering.
    vert_spacing : int
        Vertical spacing for layout purposes.
    text : str
        The current input text entered by the user.
    font : pygame.Font
        Font object for rendering text.
    img : pygame.Surface
        A surface for drawing the trigger symbol (a 64x64 rectangle).
    disp_image : Selectable
        A selectable object representing the trigger's display image.
    """

    def __init__(self, config):
        """
        Initializes the TriggerBox with a configuration.

        Parameters:
        -----------
        config : dict
            A configuration dictionary containing the rectangle size and other parameters.
        """
        # Initialize the Region class with the 'rect' config parameter
        Region.__init__(self, *config['rect'])

        # Set offsets and vertical spacing
        self.offset = [10, 10]
        self.vert_spacing = 10

        # Initialize text and font for input handling and display
        self.text = ""
        self.font = pygame.font.Font(None, 32)

        # color picker for setting trigger colors
        self.color_picker_size = 200
        self.color_picker_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 150, 
                                             self.color_picker_size, self.color_picker_size)
        #self.color_display_rect = [self.color_picker_pos[0],
                                  #self.color_picker_pos[1] + self.color_picker_size + self.vert_spacing,
                                  #self.color_picker_size,
                                  #50]
        self.color = (20, 240, 120)
        self.color_picker = self.create_color_picker(self.color_picker_size)

        # Create a 64x64 image (a green rectangle) as a trigger symbol
        self.trigger_selection_size = 64
        self.img = pygame.Surface((self.trigger_selection_size, 
                                   self.trigger_selection_size))
        
        # Create a selectable display image for the trigger symbol
        self.disp_image = Selectable(self.img, "trigger", [10, 0], _id="")
        self.disp_image.set_pos([10, 10])

        self.update_trigger_selection_display()


        #===== Show blinking bar =====#
        self.timer = 0
        self.MAX_TIMER = 45
        self.show_bar = True

        #===== Handle Backspace =====#
        self.backspace = False
        self.ctrl = False # my favorite keyboard shortcut
        self.backspace_timer = 0
        self.BACKSPACE_TIMER_MAX = 10
        self.BACKSPACE_TIMER_SHORT = 4



    def update_trigger_selection_display(self):
        pygame.draw.rect(self.img, self.color, 
                         (0, 0, self.trigger_selection_size, self.trigger_selection_size))
        #self.disp_image.set_img(self.img)

    def create_color_picker(self, size):
        """
        Creates a color picker for changing the color of the trigger

        Parameters:
        ----------
        size : int
            The length of one side of the color picker
        """
        surface = pygame.Surface((size, size))
        for y in range(size):
            for x in range(size):
                r = x * 255 // size
                g = y * 255 // size
                b = 255 - ((x + y) * 255 // (2*size))  # Dynamic blue component
                try:
                    surface.set_at((x, y), (r, g, b))
                except:
                    print(x, y, b)

        return surface
    
    def update_color_picker(self, pos):
        # if the user is hovering over the color picker and clicks
        if self.color_picker_rect.collidepoint(pos) and self.builder.clicked:
            x, y = pos[0] - self.color_picker_rect.x, pos[1] - self.color_picker_rect.y
            self.color = self.color_picker.get_at((x, y))
            self.update_trigger_selection_display()
    
    def draw_color_picker(self, screen):
        screen.blit(self.color_picker, self.color_picker_rect.topleft)
        #pygame.draw.rect(screen, self.color, self.color_display_rect)

    def draw_symbol(self, pos, state, screen):
        """
        Draws the trigger symbol on the screen.

        Parameters:
        -----------
        pos : tuple
            The mouse position on the screen.
        state : list
            The state of mouse buttons (pressed or released).
        screen : pygame.Surface
            The screen surface to draw on.
        """
        # Update and draw the selectable display image on the screen
        self.disp_image.update(pos, state, screen, True)

    def handle_text(self, event):
        """
        Handles keyboard input for text entry. This function allows the user to input, delete, or clear text.

        Parameters:
        -----------
        event : pygame.event.Event
            The keyboard event for handling text input.
        """
        if event.type == pygame.KEYDOWN:
            # Handle backspace to delete the last character
            if event.key == pygame.K_BACKSPACE:
                self.backspace = True
            elif event.key == pygame.K_LCTRL:
                self.ctrl = True
            # Handle return (Enter) key to set the display image's ID to the current text
            elif event.key == pygame.K_RETURN:
                self.disp_image.set_id(self.text)
            # Handle delete key to clear the text and reset the display image's ID
            elif event.key == pygame.K_DELETE:
                self.text = ""
                self.disp_image.set_id(self.text)
            # Handle general text input
            else:
                self.text = (self.text + event.unicode)[:10]
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspace = False
                self.backspace_timer = 0

            elif event.key == pygame.K_LCTRL:
                self.ctrl = False

    def handle_backspace(self):
        if self.backspace:

            if self.ctrl:
                self.clear_text()

            elif self.backspace_timer == 1:
                self.text = self.text[:-1]
                self.backspace_timer = self.BACKSPACE_TIMER_SHORT

            elif self.backspace_timer <= 0:
                self.text = self.text[:-1]
                self.backspace_timer = self.BACKSPACE_TIMER_MAX

            else:
                self.backspace_timer -= 1
            

    def clear_text(self):
        """
        Clears the current text input.
        """
        self.text = ""

    def draw_waiting_bar(self):
      self.timer += 1
      if self.timer % self.MAX_TIMER == 0:
         self.show_bar = not self.show_bar
      
      if self.show_bar:
          return self.text + "|"
      return self.text
         

    def select_selectables(self):
        """
        Manages the selection of the selectable display image. If selected, it updates the builder
        with the current selectable object. If deselected, it clears the selection from the builder.
        """
        select_any = False
        if self.disp_image.selected:
            select_any = True
            # If the image was just selected, notify the builder to select the image
            if not self.disp_image.just_selected:
                self.disp_image.just_selected = True
                self.builder.add_to_db(_id=self.text, img=self.img.copy())
                self.builder.select(BuilderObject(img=self.img, group=self.disp_image.group, 
                                                  _id=self.text, autotilable=False))
        else:
            self.disp_image.just_selected = False
        
        # If no image is selected, clear the builder's selected object
        if not select_any and self.builder.selected is not None:
            del self.builder.selected
            self.builder.select(None)

    def draw_text_display(self, screen):
        """
        Draws the input text on the screen.

        Parameters:
        -----------
        screen : pygame.Surface
            The screen surface to draw the text on.
        """
        # Draw a blue rectangle for the text display area
        pygame.draw.rect(screen, (50, 125, 168), (10, 100, 150, 30))
        # Render the text and blit it onto the screen
        render_txt = self.draw_waiting_bar()
        txt = self.font.render(render_txt, True, (255, 255, 255))
        screen.blit(txt, (15, 105))

    def __str__(self):
        """
        Returns the string representation of the TriggerBox.

        Returns:
        --------
        str
            A string indicating this is a "trigger" box.
        """
        return "trigger"

    def update(self, pos, state, rel, screen):
        """
        Updates the TriggerBox by drawing it on the screen, selecting interactable elements,
        and rendering the trigger symbol and input text.

        Parameters:
        -----------
        pos : tuple
            The mouse position on the screen.
        state : list
            The state of mouse buttons (pressed or released).
        rel : tuple
            The relative mouse movement.
        screen : pygame.Surface
            The screen surface to draw on.
        """
        # Draw the base region
        self.draw(screen)
        # Manage selectable elements
        self.select_selectables()
        # Draw the trigger symbol and input text
        self.draw_symbol(pos, state, screen)
        self.draw_text_display(screen)
        self.handle_backspace()

        # handle the color picker
        self.update_color_picker(pos)
        self.draw_color_picker(screen)
