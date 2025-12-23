import pygame

from scripts.rendering.camera import Camera
from scripts.tiles.tilemap import Tilemap
from scripts.entities.player import Player

class PynamoGame:
    def __init__(self):
         #===== Initialize Pygame =====#
        pygame.init()

        self.camera = Camera(0,0, debug_mode=False)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pynamo") # load from config

        self.tilemap = Tilemap()
        self.player = Player()

pyn = PynamoGame()