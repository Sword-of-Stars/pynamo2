import pygame

from scripts.entities.entity import Entity

class Trigger(Entity):
    def __init__(self, layer=-1, _id="", config={}, pos=(0,0), rect=(0,0,64,64), color=(255,100,100)):
        super().__init__(type="trigger", pos=pos)

        self.rect = pygame.Rect(*rect)
        self.original_rect = self.rect.copy()

        self.layer = layer
        self.color = color
        self.visible = False

        #===== Load Attributes =====#
        self.id = _id
        self.condition = config["condition"]
        self.effect = config["effect"]
        self.description = config["description"]

    def check_condition(self, player):
        if player.collides_with(self):
            self.color = (100,100,255)
        else:
            self.color = (255,100,100)

    def draw(self, camera):
        pygame.draw.rect(camera.display, self.color, self.rect)
    
    def update(self, camera, player):
        self.check_condition(player)
        self.move_camera(camera)
