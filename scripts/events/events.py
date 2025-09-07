import pygame

# implement blocking later for optimization

class EventHandler():
    def __init__(self, game):
        self.game = game

        self.arrow_keys = {
            "right":0,
            "left":0,
            "up":0,
            "down":0
        }

        self.zoom = {
            "+": 0,
            "-": 0
        }


    def get_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                

            elif event.type == pygame.KEYDOWN:

                #===== Arrow Keys =====#
                # assign priority:
                # 0 - not pressed
                # 1 - pressed, low priority
                # 2 - pressed, high priority
                if event.key == pygame.K_UP:
                    self.arrow_keys["up"] = 2
                    if self.arrow_keys["down"] == 2:
                        self.arrow_keys["down"] = 1
                elif event.key == pygame.K_DOWN:
                    self.arrow_keys["down"] = 2
                    if self.arrow_keys["up"] == 2:
                        self.arrow_keys["up"] = 1
                elif event.key == pygame.K_LEFT:
                    self.arrow_keys["left"] = 2
                    if self.arrow_keys["right"] == 2:
                        self.arrow_keys["right"] = 1
                elif event.key == pygame.K_RIGHT:
                    self.arrow_keys["right"] = 2
                    if self.arrow_keys["left"] == 2:
                        self.arrow_keys["left"] = 1


            elif event.type == pygame.KEYUP:
                
                #===== Arrow Keys =====#
                if event.key == pygame.K_UP:
                    self.arrow_keys["up"] = 0
                    if self.arrow_keys["down"] == 1:
                        self.arrow_keys["down"] = 2
                elif event.key == pygame.K_DOWN:
                    self.arrow_keys["down"] = 0
                    if self.arrow_keys["up"] == 1:
                        self.arrow_keys["up"] = 2
                elif event.key == pygame.K_LEFT:
                    self.arrow_keys["left"] = 0
                    if self.arrow_keys["right"] == 1:
                        self.arrow_keys["right"] = 2
                elif event.key == pygame.K_RIGHT:
                    self.arrow_keys["right"] = 0
                    if self.arrow_keys["left"] == 1:
                        self.arrow_keys["left"] = 2