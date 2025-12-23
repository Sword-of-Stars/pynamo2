import pygame

from scripts.game.states.state_machine import State
from scripts.tiles.tilemap import Tilemap
from scripts.assets.background import Background
from scripts.entities.snake import Snake
from scripts.rendering.camera import Camera
from scripts.entities.player import Player

from scripts.utils.load_level import load_level_updated
from scripts.utils.misc import flatten_dict, flatten

class Main(State):
    def __init__(self, game=None):
        super().__init__()

        self.game = game
        self.camera: Camera = game.camera
        self.player: Player = game.player

        self.tilemap = Tilemap()

        # TODO: load all of these elsewhere, not here
        self.level_data = load_level_updated("data/levels/level_1.json", self.tilemap)
        self.obstacles = self.level_data["obstacles"]
        self.triggers = self.level_data["triggers"]

        self.backgrounds = Background({"nightsky":"data/images/nightsky.png"}, current_background="nightsky")

        self.background = pygame.image.load("data/images/background.png").convert_alpha()
        self.background = pygame.transform.scale_by(self.background, 2)

        self.enemies = [Snake(pos=(100,-280))]

    def on_first(self):
        self.game.camera.set_visible()


    def run(self):
        '''
        Performs a single frame update
        '''

        self.game.clock.tick(60)

        self.game.event_handler.get_events()

        self.camera.fill()

        self.player.update(self.game.event_handler.arrow_keys, 
                           self.camera.get_relevant_obstacles(self.player, self.obstacles))
        
        dx, dy = self.camera.move(self.player)
        self.player.move_camera(self.camera, dx, dy)
        self.camera.to_render(self.player)

        for obstacle in flatten_dict(self.obstacles):
            obstacle.update(self.camera)
        
        for obstacle in self.camera.get_rendered_obstacles(self.obstacles):
            self.camera.to_render(obstacle)

        for trigger in self.triggers:
             trigger.update(self.camera, self.player)
             self.camera.to_render(trigger)

        for enemy in self.enemies:
            enemy.move_camera(self.camera, dx, dy) # move camera must be before update, otherwise things get weird
            enemy.update(self.camera.get_relevant_obstacles(enemy, self.obstacles))

            self.camera.to_render(enemy)

        #self.camera.display.blit(self.background, (0,-100)) # should handle backgrounds natively with to_render

        self.camera.draw_world()

        self.camera.update(self.game.clock.get_fps())