import pygame, sys

from ..gui_elements.regions import WorldBox, ScrollBox, TextBox, ImageBox, BlankRegion, StaticSelectBox, TriggerBox
from ..gui_elements.elements import ImgButton_base, Checkbox
from ..gui_elements.folder_nav import save_file, exit_gui
from ..builder import Builder
from ..misc.core_functions import load_json, get_mouse_info

class GUI:
    '''
    Handles the UI elemnts the player interacts with
    '''
    def __init__(self):
        # pages are of the form str:Page
        self.pages = {}
        self.current_page = None

        # I don't know what builder does
        self.builder = Builder(self)

        #===== Initialize pygame =====#
        pygame.init()
        WIDTH, HEIGHT = 1200, 750
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def init_builder(self):
        '''
        Initialize the builder header and world regions 
        '''
        self.builder.set_regions()

    def set_screen(self, screen):
        self.screen = screen

    def get_current_page(self):
        '''
        Returns the current page
        '''
        return self.pages[self.current_page]

    def add_page(self, page):
        '''
        Add a page to the GUI's collection of stored pages
        '''
        self.pages[page.name] = page

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui.exit()

            elif event.type == pygame.MOUSEWHEEL:
                gui.handle_scroll(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gui.builder.set_click(True)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gui.exit()
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    gui.builder.change_brush_size(-1)
                elif event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:
                    gui.builder.change_brush_size(1)

                gui.handle_button(event)

            elif event.type == pygame.KEYUP:
                gui.handle_button(event)

    def handle_scroll(self, event):
        '''
        Sends mouse scroll events to the relevant page

        NOTE: how is the page being detected?
        '''
        pos = get_mouse_info()[2]
        if self.current_page != None:
            self.pages[self.current_page].handle_scroll(event, pos)

    def handle_button(self, event):
        self.builder.handle_button(event)

    def update(self):
        rel, state, pos = get_mouse_info()
        if self.current_page != None: # Maybe make a default page
            self.pages[self.current_page].update(pos, state, rel, self.screen)

        pygame.display.update()

    def exit(self):

        if exit_gui():
            output_path = save_file()
            self.builder.save_map(output_path)

        pygame.quit()
        sys.exit()

    def run(self):
        self.screen.fill((0,0,0))
        self.clock.tick(60)

        pygame.display.set_caption(f"Level Editor v2.0: {self.current_page}")  

        self.handle_events()
        self.update()


class Page():
    '''
    The screen the player sees, sort of
    like a tab in a browser
    '''
    def __init__(self, config_path):
        self.config_path = config_path

        self.regions = {}
        self.load()

        self.gui = gui
        self.gui.add_page(self)

    def load(self):
        '''
        Initializes all regions in the page
        '''
        self.config = load_json(self.config_path)
        self.name = self.config['name']

        # Define a mapping from region types to their corresponding classes
        region_classes = {
            'blank': BlankRegion,
            'text': TextBox,
            'world': WorldBox,
            'image': ImageBox,
            'scroll': ScrollBox,
            'button': ImgButton_base,
            'checkbox': Checkbox,
            'static': StaticSelectBox,
            'trigger': TriggerBox,
        }

        for region in self.config['regions']:
            region_type = region['type']
            
            # Check if the region type is valid
            if region_type in region_classes:
                self.regions[region["ID"]] = region_classes[region_type](region)
            else:
                print(f"'{region_type}' is not a valid region type.")

            # set region visibility
            if "visible" in region:
                self.regions[region["ID"]].visible = bool(region["visible"])

        self.regions = dict(sorted(self.regions.items()))

    def handle_scroll(self, event, pos):
        for _, region in self.regions.items():
            if region.visible:
                region.scroll_event(event, pos)

    def update(self, pos, state, rel, screen):
        for _, region in self.regions.items():
            if region.visible:
                region.update(pos, state, rel, screen)
        gui.builder.update(pos, state, screen)
    
gui = GUI()
