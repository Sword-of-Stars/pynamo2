import pygame

from ...gui_elements.elements import Selectable, BuilderObject
from ...gui_elements.region import Region

from ...builder.builder_functions import get_path_id, get_images_from_db

class ScrollBox(Region):
      """
      Creates a box that can display a scrolling assortment of assets
      Inherits from Region

      Methods
      -------
      scroll_items
         Draws the desired images onto a subsurface in the proper position
      update
         Displays the scrolled assets
      """
      def __init__(self, config):
         """
         Inheritance
         -----------
         Region
            A versatile class describing boxy regions for UI elements

         Parameters
         ----------
         rect : tuple
            Describes the x, y, width, height of the scrollbox
         orientation : str 
            (deprecated feature)
            Determines the layout of the assets in the scrollbox (linear or box)

         Attributes
         ----------
         subsurface : pygame.Surface
            Subsurface onto which scrolled images are drawn
         subsurface_colorkey : tuple
            Colorkey for the subsurface, currently set to obscure color
         scroll : int
            How far along the player has scrolled 
            0 is the default position, increases as user scrolls up
         scroll_max : int
            The maximum vertical distance the user can scroll
         images : dict
            A dictionary containing information on all images in scroll box
            Includes "img", "pos", and "rect"
         selected : unknown data type
            Whichever image is selected
         """
         Region.__init__(self, *config['rect'])

         self.path_id = ""
         self.id_info = {'method':"", 'path':""}

         self.images = []

         # Create the subsurface
         self.subsurface = pygame.Surface((self.rect[2]-2, self.rect[3]-2))
         self.subsurface_colorkey = (0,0,1)

         # Set positioning and spacing parameters
         self.scroll = 0
         self.scroll_max = 0
         self.speed = 10
         self.selected = None

         self.get_images(config)

      def get_images(self, config):
         self.images = []
         self.load_images(config)
         self.create_selectables(config)
         
      def set_rects(self):
         for img in self.images:
            rect = img['img'].get_rect()
            img['rect'] = pygame.Rect(self.rect.x+img['offset'][0], 
                                    self.rect.y+img['offset'][1],
                                    rect[2], rect[3])

      def load_images(self, config):
         #if config['method'] == 'spritesheet':
            # Generate batch ID
            #self.id_info['method'] = "ss"
         path_id = get_path_id(f"{self.builder.path_to_save}/config.json", config['spritesheet'])
         self.images = get_images_from_db(self.builder.database, path_id)
            #self.id_info['path'] = path_id
         
         if path_id != self.path_id:
            self.scroll = 0
         self.path_id = path_id

      def create_selectables(self, config):
         group = config['group']
         offset = (10,10)#config['image_start_offset']#(20,-180)
         vertical_spacing = 10 #config['vert_offset']#10
         height = offset[1]
         new_list = []

         for index, img in enumerate(self.images):
            _id = f"ss;{self.path_id};{index}"
            self.builder.add_to_db(_id, img)
            new = Selectable(img, group, hover_offset=[10,0], _id=_id, autotilable=bool(config['auto?']))

            x = offset[0]
            y = height
            height += new.rect.height+vertical_spacing

            new.set_pos((x,y))
            new_list.append(new)

         self.images = [x for x in new_list]

         self.scroll_max = max(0, height - self.rect.height) # This has not been tested, further analysis required

      def scroll_items_select(self, pos, state):
         self.scroll = min(max(self.scroll, 0), self.scroll_max)
         
         # Prepares the subsurface for receiving the images
         self.subsurface.fill(self.subsurface_colorkey)
         self.subsurface.set_colorkey(self.subsurface_colorkey)
         self.subsurface.convert_alpha()

         for img in self.images:
            img.rect.y = img.pos[1]-self.scroll
            new_pos = (pos[0]-self.rect.x, pos[1]-self.rect.y)
            img.update(new_pos, state, self.subsurface, self.rect.collidepoint(pos))

      def scroll_event(self, event, pos):
         if self.rect.collidepoint(pos):
            self.scroll -= event.y*self.speed

      def select_selectables(self):
         select_any = False
         for img in self.images:
            if img.selected:
               select_any = True
               if not img.just_selected:
                  img.just_selected = True
                  self.builder.select(BuilderObject(img.img, img.group, img.id, img.autotilable, size=self.builder.brush_size))
               
            else:
               img.just_selected = False
            
         if not select_any:
            if self.builder.selected != None:
               del self.builder.selected
               self.builder.select(None)

      def blit_subsurface(self, screen):
         x, y = self.rect.topleft
         screen.blit(self.subsurface, (x+1, y+1))

      def update(self, pos, state, rel, screen):
         self.draw(screen) # Inherited from Region
         self.scroll_items_select(pos, state)
         self.blit_subsurface(screen)
         self.select_selectables()
