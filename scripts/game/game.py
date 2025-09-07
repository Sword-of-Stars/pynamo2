import pygame, sys

from scripts.game.states.state_machine import state_machine
from scripts.rendering.camera import Camera

#===== Load in the Centralized Asset Manager =====#
from scripts.asset_manager import AssetManager

#===== Import our Relevant States =====#
from scripts.game.states.main import Main
from scripts.game.states.menu import Menu

#===== Player =====#
from scripts.entities.player import Player

#===== Events =====#
from scripts.events.events import EventHandler


class Game():
    '''
    Manager object for the entire game

    'Big Daddy' - don't be afraid to put stuff here

    Each state in the state machine contains a game state,
    such as a menu, main loop, credits, cutscene, etc.
    '''
    def __init__(self, config=None):
        '''
        Any 'global' variables that the states need to access should 
        accessible from the Game class
        This includes:
        1) camera
        2) running
        3) ...
        '''
        #===== Initialize Pygame =====#
        pygame.init()
        self.camera = Camera(0,0, debug_mode=False)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pynamo") # load from config

        #===== Player =====#
        self.player = Player()

        #===== Define States =====#
        self.state_machine = state_machine
        self.states = {
            "main": Main(game=self),
            "menu": Menu(game=self)
        }
        self.state_machine.init_states(states=self.states)
        self.state_machine.set_state("main") # begin on menu state

        self.running = True

        #==== Events =====#
        self.event_handler = EventHandler(self)


    def run(self):
        '''
        Run the state machine, which handles each portion of
        the gameplay

        NOTE: Need a good way for self.running to be toggled
        '''
        
        while self.running:               
            self.state_machine.run()

        pygame.quit()
        sys.exit()