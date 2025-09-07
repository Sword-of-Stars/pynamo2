import pygame
import random
import itertools # hello, Dr. Dougherty
import math

from scripts.utils.game_math import sign, distance
from scripts.entities.creatures.inverse_kinematics import Arm

class IKCreature:
    """
    defines a creature driven by inverse kinematics
    """

    def __init__(self, pos=(0,0), n_arms=3, size=10):
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.color = (255,0,0)

        self.rect = pygame.rect.Rect(0,0,size,size)
        self.rect.center = pos
        self.layer = 1

        self.vel = pygame.Vector2(0,0)
        self.speed = 3

        self.n_arms = n_arms
        self.arms: list[Arm] = []
        for arm in range(self.n_arms):
            self.arms.append(Arm(self.pos, 2, 80))
        self.reach = self.arms[0].length*0.9

        self.grabbable = []

        # define optimal positions
        self.optimal_positions = []

    def calculate_optimal_positions(self):
        # descriptive enough, I guess, maybe need offset
        self.optimal_positions = [pygame.Vector2(self.rect.center) + self.reach*pygame.Vector2(math.cos(math.pi*2/self.n_arms*i), 
                                                            math.sin(math.pi*2/self.n_arms*i)) 
                                                            for i in range(self.n_arms)]


    def collides_with(self, entity):
        return self.rect.colliderect(entity.rect)

    def draw_grab_radius(self, camera):
        pygame.draw.circle(camera.display, (100,100,100), self.rect.center, self.arms[0].length)

    def get_grabbable(self, obstacles):
        self.grabbable = []
        for obstacle in obstacles:

            for position in obstacle.exposed_edges:
                if distance(position, self.rect.center) < self.reach:

                    for obs in obstacles:
                        if obs != obstacle:
                            if obs.rect.clipline(self.rect.center, position):
                                break
                    else:
                        self.grabbable.append(position)
                        

    def draw_grabbable(self, camera):
        for postiion in self.grabbable:
            pygame.draw.circle(camera.display, (255,0,0), postiion, 5)

        for arm in self.arms:
            pygame.draw.circle(camera.display, (100,100,155), arm.target, 8)


    def evaluate_position(self):
        # calculate the optimal position for each arm
        for i, arm in enumerate(self.arms):
            arm = self.arms[i]

            # if the arm can reach the target
            #if arm.has_target and arm.distance_root_to_target() <= arm.length:
                #continue
            arm.has_target = False

            # if the arm doesn't have a target and there's a valid target in range
            if not arm.has_target and self.grabbable != []:
                # set the arm's target to the one closest to the optimal position
                best_target = min(self.grabbable, key=lambda x: distance(self.optimal_positions[i], x))
                arm.set_target(best_target)
                arm.has_target = True

            else:
                arm.set_target(self.optimal_positions[i])
                arm.has_target = False # idle, need better coding

    def draw(self, camera):

        self.draw_grabbable(camera)

        for arm in self.arms:
            arm.set_root(self.rect.center)
            arm.update(camera)

        pygame.draw.circle(camera.display, self.color, self.rect.center, self.size)

        for pos in self.optimal_positions:
            pygame.draw.circle(camera.display, (255,255,0), pos, 10)

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

        for arm in self.arms:
            arm.target -= pygame.Vector2(int(camera.speed * dx), int(camera.speed * dy))

    def update(self, arrow_keys, obstacles):

        self.vel[0] = sign(arrow_keys["right"] - arrow_keys["left"])
        self.vel[1] = sign(arrow_keys["down"] - arrow_keys["up"])
        if self.vel != [0,0]:
            self.vel = self.vel.normalize() * self.speed

        self.pos += self.vel
        self.rect.center += self.vel

        self.get_grabbable(obstacles)
        self.calculate_optimal_positions()
        self.evaluate_position()
