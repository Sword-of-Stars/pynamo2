import os

from ...gui_elements.region import Region


class FolderNav(Region):
   def __init__(self, config):
      Region.__init__(self, *config['rect'])

      self.cwd = os.getcwd()
      self.dir = config['dir']

   def get_items(self):
      print(os.listdir(f"{self.cwd}/{self.dir}"))

   def create_cells(self):
      pass

   def update(self, pos, state, rel, screen):
      self.draw(screen)

      if state[0]:
         self.get_items()
