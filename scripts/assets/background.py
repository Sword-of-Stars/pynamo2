import pygame

class Background():
    def __init__(self, images={}, current_background=""):

        self.images = {}
        for key, item in images.items():
            self.images[key] = pygame.image.load(item).convert_alpha()

        self.current_background = current_background
        self.current_image = self.images[self.current_background]
        self.display_image = pygame.transform.scale_by(self.current_image, 2)

        self.layer = -10
        self.rect = self.current_image.get_rect()

    def set_current_background(self, bkg):
        self.current_background = bkg
        self.current_image = self.images[self.current_background]
        self.display_image = pygame.transform.scale_by(self.current_image, 2)


    def draw(self, camera):
        camera.display.blit(self.display_image, (0,0))