import pygame

from scripts.asset_manager import AssetManager

class Entity():
    '''
    An entity is any sprite in the game
    '''

    images = [] # make this a class attribute so I only ever load images once
    initialized = False

    def __init__(self, type, pos):

        #assert self.initialized, f"[ERROR] entity {type} has not been initialized"
        
        self.type = type
        self.pos = pos

        # rendering options
        self.opacity = 255
        self.scale = [1, 1]
        self.rotation = 0
        self.flip = [False, False]
        self.visible = True

    def move_camera(self, camera):
        '''
        This is used for static entities, like obstacles and tiles
        '''
        self.rect.x = self.original_rect.x - camera.x
        self.rect.y = self.original_rect.y - camera.y


    @classmethod
    def load_data(cls, data):
        # sets attributes from data json, mainly just images
        cls.initialized = True
        

class PhysicsEntity(Entity):
    """
    A physics entity, irrespective of the type of game
    """
    def __init__(self, type, pos):
        super().__init__(type, pos)

        self.collide_directions = {'up': False, 'down': False, 'right': False, 'left': False}

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

    def physics_move(self, obstacles):
        self.collide_directions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.rect.x += self.vel[0]
        self.collision_check((self.vel[0], 0), obstacles)
        self.rect.y += self.vel[1]
        self.collision_check((0, self.vel[1]), obstacles)

        if self.collide_directions["down"]:
            self.can_jump = True

    def collision_check(self, movement, obstacles):
        rect = self.rect
        for obstacle in obstacles:

            if rect.colliderect(obstacle.rect):
                if movement[0] > 0:
                    rect.right = obstacle.rect.left
                    self.vel[0] = 0
                    self.collide_directions['right'] = True
                if movement[0] < 0:
                    rect.left = obstacle.rect.right
                    self.vel[0] = 0
                    self.collide_directions['left'] = True
                if movement[1] > 0:
                    rect.bottom = obstacle.rect.top
                    self.vel[1] = 0
                    self.collide_directions['down'] = True
                if movement[1] < 0:
                    rect.top = obstacle.rect.bottom
                    self.vel[1] = 0
                    self.collide_directions['up'] = True

            if rect.x != self.rect.x:
                self.rect.x = rect.x
            if rect.y != self.rect.y:
                self.rect.y = rect.y

            rect = self.rect

    def collides_with(self, entity):
        return self.rect.colliderect(entity.rect)

