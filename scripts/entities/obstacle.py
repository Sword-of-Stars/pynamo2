import pygame

from scripts.entities.entity import Entity

class Obstacle(Entity):
    def __init__(self, pos=(0,0), color=(255,255,0), rect=(100,100,100,100)):
        super().__init__(type="obstacle", pos=pos)

        self.rect = pygame.Rect(*rect)
        self.original_rect = self.rect.copy()

        self.color = color
        self.layer = 0

    def draw(self, camera):
        pygame.draw.rect(camera.display, self.color, self.rect)

    def update(self, camera):
        self.move_camera(camera)

class TileObstacle(Entity):
    def __init__(self, pos=(0,0), color=(255,255,0), rect=(0,0,64,64), layer=0, img=None, exposed_edges=[]):
        super().__init__(type="obstacle", pos=pos)

        self.rect = pygame.Rect(*rect)
        self.original_rect = self.rect.copy()

        self.color = color
        self.layer = layer

        if img == None:
            self.img = pygame.Surface(rect[2:])
            pygame.draw.rect(self.img, self.color, self.rect)
        else:
            self.img = img

    def draw(self, camera):
        camera.display.blit(self.img, self.rect[:2])
    
    def update(self, camera):
        self.move_camera(camera)

