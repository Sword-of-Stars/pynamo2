import pygame
import importlib

from ...gui_elements.region import Region

class TextBox(Region):
   '''
   For optimization and practice, find a way to save the font
   to the elements to avoid repeatedly loading the text
   '''
   def __init__(self, config):
      Region.__init__(self, *config['rect'])
      self.config = config
      self.movable_text = bool(config['movable'])

      self.init_text()
      self.set_functions()

      self.selected = None
      self.horiz_shift = 10

   def init_text(self):
      self.rendered_texts = {}

      for item in self.config['text']:
         msg, pos, rect = self.render_text(item)

         func = ""
         args = []
         if 'function' in item.keys():
            func = item['function']

            args = [getattr(self, arg) for arg in item['self_args']]
            for i in item['args']:
               args.append(i)

         # Should I move this to an object? I'm repeating a lot of code in this gui system
         # Future versions should streamline functions, selectables
         self.rendered_texts[item['name']] = {'text':item['text'],'rendered_text':msg, 'pos':pos, 
                                              'anal':item['anal'], 'color':item['color'],
                                              'rect':rect, 'size':item['size'], 'active':False, 'function':func,
                                              'args':args}

   def set_functions(self):
      module = importlib.import_module("config.functions") 
      for _, txt in self.rendered_texts.items():
         if hasattr(module, txt['function']):
            function = getattr(module, txt['function'])
            txt['function'] = function
         else:
            if txt['function'] != "":
               print(f"Function {txt['function']} not found")
            txt['function'] = None

   def draw_text(self, pos, state, screen):
      already_hovering = False
      for key, i in self.rendered_texts.items():
         x, y = i['pos']
         if not already_hovering:
            if i['rect'].collidepoint(pos):
               already_hovering = True
               if self.movable_text: x += self.horiz_shift
               if state[0] and self.selected != i:
                  self.selected = i
                  if i['function'] != None:
                     i["function"](*i['args'])
   
         screen.blit(i['rendered_text'], (x,y))


   def render_text(self, item):
      font = pygame.font.Font("pynamogui/data/at01.ttf", item['size'])
      msg = font.render(str(item['text']), item['anal'], item['color'])
      pos = (item['pos'][0]+self.rect.x,
                item['pos'][1]+self.rect.y)
      rect = msg.get_rect(x=pos[0], y=pos[1])

      return msg, pos, rect


   def add_text(self, text, size, color, pos, name, anal=False):
      font = pygame.font.Font("pynamogui/data/at01.ttf", size)
      msg = font.render(text, anal, color)
      pos = (pos[0]+self.rect.x,
             pos[1]+self.rect.y)
      rect = msg.get_rect(x=pos[0], y=pos[1])
      self.rendered_texts[name] = {'text':text, 'rendered_text':msg, 'pos':pos, 
                                   'size':size,'anal':anal,'color':color,
                                   'rect':rect, 'active':False, 'function':""}

   def modify_text(self, txt_name, value):
      """
      Currently only modifies the text value
      """
      item = self.rendered_texts[txt_name]
      item['text'] = value

      msg, pos, rect = self.render_text(item)
      item['rendered_text'] = msg
      item['rect'] = rect


   def update(self, pos, state, rel, screen):
      self.draw(screen)
      self.draw_text(pos, state, screen)
