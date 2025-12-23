import pygame

from scripts.game.states.state_machine import State
from scripts.ui.button import load_buttons_from_config

class Menu(State):
    '''
    Ideally, this is just a placeholder, and eventually 
    gets taken out of Pynamo

    Pynamo is not a game in and of itself, it's an
    engine/framework
    '''
    def __init__(self, game=None):
        super().__init__()

        self.game = game

        self.buttons = load_buttons_from_config("lab/config.json")
        self.background = pygame.image.load("data/images/TitleScreen.png").convert_alpha()
        self.background = pygame.transform.scale_by(self.background, 0.6)

    def on_first(self):
        self.game.camera.set_visible()

    def run(self):
        '''
        Performs a single frame update
        '''
        self.game.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

        self.game.camera.fill()

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0] # change to an event

        for button in self.buttons:
            if button.update(mouse_pos, mouse_click):
                self.state_machine.set_state(*button.args)

        self.game.camera.display.blit(self.background, (-40,0))

        for button in self.buttons:
            self.game.camera.to_render(button)

        self.game.camera.draw_world()
        self.game.camera.update()




