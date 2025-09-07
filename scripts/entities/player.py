import pygame

from scripts.entities.entity import PhysicsEntity
from scripts.asset_manager import AssetManager

from scripts.utils.game_math import sign

class Player(PhysicsEntity):
    '''
    A class for the player. Note that this isn't meant to
    handle player data, just their sprite
    '''
    def __init__(self):
        super().__init__(type="player", pos=(0,0))

        self.rect = pygame.Rect(0,0,48,32)
        self.rect.center = self.pos
        self.color = (255,0,0)
        self.layer = 1
        self.speed = 8
        self.ACCEL = 2
        self.DECEL = 1
        self.MAX_FALL_SPEED = 20
        
        self.vel = pygame.Vector2((0,0))

        self.JUMP_SPEED = 20
        self.can_jump = True

        self.animations = AssetManager.load_asset("player", "spritesheet", data=["data/images/Fox Sprite Sheet.png", 32, 32,
                                         [True, True, True, False, False, False, False],
                                         self.rect,
                                         ["idle", "idle2", "move", "attack", "damage", "sleep", "death"]])
        self.state = "idle"
        self.facing = False
        

    def draw(self, camera):
        #pygame.draw.rect(camera.display, self.color, self.rect)
        
        self.animations[self.state].play()
        self.animations[self.state].draw(camera, (self.rect.left-40, self.rect.top-96), flip=self.facing)

    def calaulate_vel(self, pressed):

        if pressed["right"] > pressed["left"]:
            self.vel[0] += self.ACCEL
            self.facing = False
        elif pressed["right"] < pressed["left"]:
            self.vel[0] -= self.ACCEL
            self.facing = True
        else:
            if abs(self.vel[0]) > 2*self.DECEL:
                self.vel[0] -= sign(self.vel[0])*self.DECEL
            else:
                self.vel[0] = 0

        if pressed["up"]:
            self.jump()
            self.can_jump = False

        if abs(self.vel[0]) > self.speed:
            self.vel[0] = sign(self.vel[0]) * self.speed 

        self.vel[1] = min(self.MAX_FALL_SPEED, self.vel[1]+1)

    def update(self, pressed, obstacles):

        if self.state != "death":
            self.calaulate_vel(pressed)
            self.physics_move(obstacles)

    