import pygame
import json
import importlib
import os

from ...gui_elements.region import Region
from ...gui_elements.elements import Selectable, BuilderObject

from ...builder.builder_functions import get_path_id, get_images_from_db

class StaticSelectBox(Region):
   # To be used for tilesets (autotile)
   # So, this thing is going to need:
   # 1) Some sort of access to tilesets to get the display image
   # 2) Interactive tile movements (slide right on hover)
   # 3) Connection to autotile algorithm

   def __init__(self, config):
      Region.__init__(self, *config['rect'])

      self.offset = [10,10]
      self.vert_spacing = 10

      #print(f"[STATIC SELECT] {self.builder.config}")
      self.images = self.load_images(config)

      if len(self.images) == 0: # placeholder on empty
         img = pygame.surface.Surface((64,64))
         self.disp_image = Selectable(img, "tile", [10,0], _id = f"ss;{self.path_id};{48}")
      else:
         self.disp_image = Selectable(self.images[-1], "tile", [10,0], _id = f"ss;{self.path_id};{48}")

      self.disp_image.set_pos((self.rect.x + self.offset[0], self.rect.y + self.offset[1]))
      self.selectables = [self.disp_image]

   def load_images(self, config):
      self.path_id = get_path_id(f"{self.builder.path_to_save}/config.json", config['spritesheet'])
      return get_images_from_db(self.builder.database, self.path_id)
   
   def draw_selectables(self, pos, state, screen):
      self.disp_image.update(pos, state, screen, True)

   def select_selectables(self):
      select_any = False
      for img in self.selectables:
         if img.selected:
            select_any = True
            if not img.just_selected:
               img.just_selected = True
               self.builder.select(BuilderObject(img.img, img.group, img.id, autotilable=True, size=self.builder.brush_size))
            
         else:
            img.just_selected = False
         
      if not select_any:
         if self.builder.selected != None:
            del self.builder.selected
            self.builder.select(None)

   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.draw_selectables(pos, state, screen)
      self.select_selectables()
