import pygame, math

from scripts.entities.entity import PhysicsEntity
from scripts.asset_manager import AssetManager

class Snake(PhysicsEntity):
    '''
    A class for the player. Note that this isn't meant to
    handle player data, just their sprite
    '''
    def __init__(self, pos):
        super().__init__(type="enemy", pos=pos)

        self.rect = pygame.Rect(0,0,32,32)
        self.rect.center = self.pos
        self.color = (255,0,0)
        self.layer = 1
        self.speed = 8
        self.ACCEL = 2
        self.DECEL = 1
        self.MAX_FALL_SPEED = 25
        
        self.vel = pygame.Vector2((0,0))

        self.JUMP_SPEED = 20
        self.can_jump = True

        self.collide_directions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.animations = AssetManager.load_asset("snake", "spritesheet", data=["data/images/Cobra Sprite Sheet.png", 32, 32,
                                         [True, True, True, False, False],
                                         self.rect,
                                         ["idle", "move", "bite", "damage", "death"]])
        self.state = "move"
        self.facing = False

        self.dir = 0
        

    def draw(self, camera):
        #pygame.draw.rect(camera.display, self.color, self.rect)
        self.animations[self.state].play()
        self.animations[self.state].draw(camera, (self.rect.left-40, self.rect.top-96), flip=self.facing)


    def calaulate_vel(self):
        self.vel[1] = min(self.MAX_FALL_SPEED, self.vel[1]+1)

    def update(self, obstacles):

        self.calaulate_vel()
        self.physics_move(obstacles)

    