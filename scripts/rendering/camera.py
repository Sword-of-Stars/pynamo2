import pygame
import random

from scripts.rendering.shaders import ShaderContext
from scripts.utils.file_io import load_json
from scripts.utils.misc import flatten

# To avoid passing 'camera' and 'screen' to every function, I'll just pass a single camera
# object instead
# All sprites will be drawn on the camera surface, and the camera display will be scaled up to the 
# screen dimensions

SIZE = 256
CHUNK_DIVISOR = 1

def screen_to_chunk(pos, offset):
    return get_chunk_id(screen_to_world(pos, offset))

def screen_to_tile(pos, offset):
    return get_tile_pos(screen_to_world(pos, offset))

def get_chunk_id(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x//divisor, y//divisor)

def get_tile_pos(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x%4, y%4)


def screen_to_world(screen_coords, offset, SIZE=SIZE, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [int(world_x//SIZE), int(world_y//SIZE)]

def world_to_screen(world_coords, offset, scale=1):
    world_x, world_y = world_coords
    offset_x, offset_y = offset
    screen_x = (world_x - offset_x)*scale
    screen_y = (world_y - offset_y)*scale
    return [screen_x, screen_y]


class Camera():
    '''
    Handles rendering with ordering and optimizes chunk rendering

    TODO: Make intuitive scaling
    TODO: Handle interpolated paths for cutscenes
    '''
    def __init__(self, x, y, scale=1.0, debug_mode=False):

        # First, load in the world data to get the screen's width and height
        world_data = load_json("data/configs/world.json")
        WIDTH, HEIGHT = world_data["WIDTH"], world_data["HEIGHT"]

        # Must be done for moderngl to have an opengl surface to reference
        # We enable the HIDDEN flag so the pygame window isn't open during loading
        pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)

        #===== Attributes =====#
        self.x = x
        self.y = y
        self.width = WIDTH
        self.height = HEIGHT
        self.scale = scale

        self.speed = 0.05 # the speed at which the camera moves

        # the list of objects to render
        # these must have the draw method and layer/rect attribute
        self.render_list = [] 

        # the main display to which items are rendered
        self.display = pygame.Surface((self.width, self.height))
        self.new_display = pygame.Surface((self.width, self.height))

        self.rect = self.display.get_rect(x=x, y=y)

        # a transparent surface for UI elements
        self.ui_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # enables use of chaders
        self.ctx = ShaderContext()

        # attributes for screen shake
        self.screen_shake = False
        self.screen_shake_x = []
        self.screen_shake_y = []

        # set debugging properties
        self.debug_mode = debug_mode
        self.font = pygame.font.SysFont("Arial", 20)

    def set_visible(self):
        '''
        Disables pygame's hidden flag

        NOTE: Maybe a better way?
        '''
        pygame.display.set_mode((self.width, self.height),  
                                pygame.OPENGL | pygame.DOUBLEBUF) 

    def reset(self, pos=(0,0)):
        '''
        Resets the camera position to (0,0)
        '''
        self.x, self.y = pos

    def fill(self):
        '''
        Clears the screen and UI surface for the next
        set of rendering
        '''
        self.render_list = []
        self.display.fill((0,0,0))
        self.ui_surf.fill((0,0,0,0))

    def set_screen_shake(self, val, magnitude=[3,1]):
        self.screen_shake = True
        self.screen_shake_x = [random.randint(-magnitude[0], magnitude[0]) for x in range(val//2)]
        self.screen_shake_x + self.screen_shake_x[::-1]

        self.screen_shake_y = [random.randint(-magnitude[1], magnitude[1]) for x in range(val//2)]
        self.screen_shake_y + self.screen_shake_y[::-1]

    def shake_screen(self):
        pos = (0,0)
        if self.screen_shake_x != [] and self.screen_shake_y != []:
            pos = (self.screen_shake_x.pop(), self.screen_shake_y.pop())

        return pos

    def set_zoom(self, zoom):
        self.scale = zoom
        

    def move(self, player):
        '''
        Allows the camera to follow the player, moving at a speed
        proportionate to the player's distance from the camera's center
        '''
        # find the distance from the player to the center of the screen
        dx = player.rect.x - self.width/2
        dy = player.rect.y - self.height/2

        # calculate new camera position using smoothing function
        self.x += int(dx * self.speed)
        self.y += int(dy * self.speed)

        return dx, dy
    
    def screen_to_chunk(self, pos):
        return get_chunk_id(screen_to_world(pos, (self.x, self.y)))
    
    def world_to_screen(self, world_coords):
        return world_to_screen(world_coords, (self.x, self.y), self.scale)

    def pos_to_tile(self, pos):
        return self.screen_to_chunk(pos), screen_to_tile(pos, (self.x, self.y))
    
    def get_chunks_in_range_from_pos(self, pos, horiz=1, vert=1):
        cx, cy = self.screen_to_chunk(pos)

        chunk_map = []
    
        for x in range(-horiz, horiz+1):
            for y in range(-vert, vert+1):
                chunk_map.append((cx+x,cy+y))
                    
        return chunk_map

    def get_visible_chunks(self):
       
        ax, ay = self.screen_to_chunk(self.rect.topleft)
        bx, by = self.screen_to_chunk(self.rect.bottomright)

        c_dx = bx-ax+1 # +1 adds a bit of buffer for seamless drawing
        c_dy = by-ay+1
        
        chunk_map = []
    
        # start at -1 for a buffer
        for x in range(-1, c_dx):
            for y in range(-1, c_dy):
                #chunk_map.append(f"{ax+x};{ay+y}")
                chunk_map.append((ax+x,ay+y))
                    
        return chunk_map
    
    def get_relevant_obstacles(self, entity, obstacles):
        relevant_chunks = self.get_chunks_in_range_from_pos(entity.rect.topleft)
        return flatten([obstacles[f"{x};{y}"] for x, y in relevant_chunks])
    
    def show_chunks(self):
        '''
        Shows the chunks being rendered on the screen
        '''
        
        chunk_map = self.get_visible_chunks()

        for chunk in chunk_map:
            x, y = chunk
            rect_x = x*SIZE - self.x
            rect_y = y*SIZE- self.y
            pygame.draw.rect(self.display, (255, 0, 0), (rect_x, rect_y, SIZE, SIZE), width=2)

    def show_debug_text(self, fps=-1.0):
        text_surf = self.font.render(f"FPS: {fps}\nNum Rendered: {len(self.render_list)}",
                                     True, (255,255,255))
        self.display.blit(text_surf, (20,20))

    def get_rendered_obstacles(self, obstacles):
        chunks = self.get_visible_chunks()
        return flatten([obstacles[f"{x};{y}"] for x, y in chunks])        
   
    def to_render(self, object):
        '''
        Adds an item to the camera's render queue

        Args:
            object (Entity): object to be rendered, must have
                             draw method, and both rect and 
                             layer attributes  
        '''

        # Remove checking after
        assert type(object.layer) is not None

        self.render_list.append(object)

    def draw_world(self):
        '''
        Draws everything in the render list to the screen 
        using appropriate ordering
        '''

        # Only draw tiles that are supposed to be on screen, eventually implement y ordering
        for item in sorted(self.render_list, key=lambda x: (x.layer, x.rect.y, x.rect.x)):
            item.draw(self)

        if self.debug_mode:
            self.show_chunks()


    def update(self, fps=-1.0):
        '''
        Handles screen shake, drawing to the screen, and handles shaders

        TODO: extend shader functionality with kwargs
        '''
        pos = self.shake_screen()

        if self.debug_mode:
            self.show_debug_text(fps)
        
        self.new_display.blit(self.display, pos)

        self.ctx.update(self.new_display, self.ui_surf)

