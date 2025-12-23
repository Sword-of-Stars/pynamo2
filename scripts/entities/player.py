import pygame

from scripts.entities.entity import PhysicsEntity
from scripts.asset_manager import AssetManager

from scripts.utils.game_math import sign

RIGHT = True
LEFT = False

class Player(PhysicsEntity):
    '''
    A class for the player. Note that this isn't meant to
    handle player data, just their sprite
    '''
    def __init__(self, _type="player", pos=(0,0)):
        super().__init__(type=_type, pos=pos)

        self.rect = pygame.Rect(0,0,48,32) # MAGIC
        self.rect.center = self.pos
        self.color = (255,0,0)
        self.layer = 1
        self.speed = 8
        self.ACCEL = 2
        self.DECEL = 1
        
        self.vel = pygame.Vector2((0,0))

        self.JUMP_SPEED = 20
        self.can_jump = True

        self.states = ["idle", "idle2", "move", "attack", "damage", "sleep", "death"]
        self.state = "idle"

        self.animations = AssetManager.load_asset("player", "spritesheet", 
                                                  data=["data/images/Fox Sprite Sheet.png", 32, 32,
                                                [True, True, True, False, False, False, False],
                                                self.rect, self.states])
        self.facing = RIGHT
        

    def draw(self, camera):
        #pygame.draw.rect(camera.display, self.color, self.rect)
        
        self.animations[self.state].play()
        self.animations[self.state].draw(camera, (self.rect.left-40, self.rect.top-96), flip=self.facing) # MAGIC

    def calaulate_vel(self, pressed):
        """
        How does the player respond to input?
        """
        pass

    def update(self, pressed, obstacles):

        if self.state != "death":
            self.calaulate_vel(pressed)
            self.physics_move(obstacles)

class PlayerPlatformer(Player):
    def __init__(self, _type="player", pos=(0,0)):
        super().__init__(_type=_type, pos=pos)

        self.MAX_FALL_SPEED = 20
        
        self.JUMP_SPEED = 20
        self.can_jump = True

    def calaulate_vel(self, pressed):

        if pressed["right"] > pressed["left"]:
            self.vel[0] += self.ACCEL
            self.facing = False
        elif pressed["right"] < pressed["left"]:
            self.vel[0] -= self.ACCEL
            self.facing = True
        else:
            if abs(self.vel[0]) > 2*self.DECEL: # BUG: what is this?
                self.vel[0] -= sign(self.vel[0])*self.DECEL
            else:
                self.vel[0] = 0

        if pressed["up"]:
            self.jump()
            self.can_jump = False

        if abs(self.vel[0]) > self.speed:
            self.vel[0] = sign(self.vel[0]) * self.speed 

        self.vel[1] = min(self.MAX_FALL_SPEED, self.vel[1]+1)

    def jump(self):
        if self.can_jump:
            self.vel[1] = -self.JUMP_SPEED

class PlayerTopDown(Player):
    def __init__(self, _type="player", pos=(0,0)):
        super().__init__(_type=_type, pos=pos)

        self.NORMAL_SPEED = 6
        self.speed = self.NORMAL_SPEED

        self.DASH_SPEED = 30
        self.DASH_TIMER_MAX = 10
        self.dash_timer = 0
        self.DASH_COOLDOWN_TIMER_MAX = 200
        self.dash_cooldown_timer = 0

    def can_dash(self):
        return self.dash_cooldown_timer == 0
    
    def dash(self):
        if self.can_dash():
            # self.state = "dash"
            self.dash_timer = self.DASH_TIMER_MAX # dash for DASH_TIMER_MAX frames
            self.speed = self.DASH_SPEED

    def is_dashing(self):
        return self.dash_timer > 0
    
    def handle_dash(self, pressed):
        if pressed["space"] == 1:
            pressed["space"] -= 1
            self.dash()

        if self.is_dashing():
            self.dash_timer -= 1
        else:
            if self.speed == self.DASH_SPEED: # first frame where the player stopped dashing
                self.dash_cooldown_timer = self.DASH_COOLDOWN_TIMER_MAX
                self.speed = self.NORMAL_SPEED

            if self.dash_cooldown_timer > 0:
                self.dash_cooldown_timer -= 1

    def calaulate_vel(self, pressed):

        # horizontal movement
        if pressed["right"] > pressed["left"]:
            self.vel[0] = 1
            self.facing = RIGHT
        elif pressed["right"] < pressed["left"]:
            self.vel[0] = -1
            self.facing = LEFT
        else:
            self.vel[0] = 0

        # vertical movement
        if pressed["down"] > pressed["up"]:
            self.vel[1] = 1
        elif pressed["down"] < pressed["up"]:
            self.vel[1] = -1
        else:
            self.vel[1] = 0

        self.handle_dash(pressed)
        if self.vel != [0,0]:
            self.vel = self.vel.normalize()*self.speed