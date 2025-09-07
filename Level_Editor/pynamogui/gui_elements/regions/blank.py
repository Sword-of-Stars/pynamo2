from ...gui_elements.region import Region

class BlankRegion(Region):
   '''
   A blank region, mainly used for spacing
   '''
   def __init__(self, config):
      Region.__init__(self, *config['rect'])