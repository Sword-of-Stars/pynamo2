import pygame
import math

from typing import Self
from scripts.utils.game_math import trig, polar_to_cartesian


###########
# Classes #
###########


class Segment():
    def __init__(self, pos: pygame.Vector2 | tuple | list, length: int | float, angle: int | float,
                 parent: Self | None = None, child: Self | None = None):
        # elementary attributes
        self.pos = pygame.Vector2(pos)
        self.length = length
        self.angle = angle

        # relative positioning
        self.start = pygame.Vector2(pos)
        self.end = polar_to_cartesian(self.start, self.angle, self.length)
        self.parent = parent
        self.child = child

        # visual components
        self.color = (0, 0, 255)
        self.width = 5

    def calculate_start(self):
        """
        sets the start point of the segment to the
        endpoint of its parent, it it exists
        """
        if self.parent is not None:
            self.start = self.parent.end

    def calculate_end(self):
        """
        calculates the new endpoint of the segment
        """
        self.end = polar_to_cartesian(self.start, self.angle, self.length)

    def draw(self, camera):
        """
        displays the segment to the camera
        """
        pygame.draw.line(camera.display, self.color, self.start, self.end, self.width)

    def update(self, camera):
        self.calculate_start()
        self.calculate_end()
        self.draw(camera)


class Arm():
    def __init__(self, pos: pygame.Vector2 | tuple | list,
                 n_segments: int, segment_len: int | float):
        # elementary attributes
        self.pos = pygame.Vector2(pos)

        # segment attributes
        self.n_segments = n_segments
        self.segment_len = segment_len
        self.segments: list[Segment] = []
        self.create_segments()
        self.length = self.n_segments * self.segment_len  # total length of arm

        # tracking
        self.target = pygame.Vector2((0, 0))
        self.has_target = False

    def create_segments(self):
        """
        creates all leg segments for the arm, from
        root (index 0) to tail (index n_segments)
        """
        for i in range(self.n_segments):

            if i == 0:  # first segment
                parent = None
                start = self.pos
            else:
                parent = self.segments[i - 1]
                parent.child = self
                start = parent.end

            s = Segment(start, self.segment_len, math.pi * 2, parent)
            self.segments.append(s)

    def set_root(self, root):
        self.pos = pygame.Vector2(root)
        self.segments[0].start = self.pos
        self.forward_kinematics()

    def set_target(self, target: pygame.Vector2 | tuple | list):
        """
        set the arm's end effector
        """
        self.target = target

    def distance_to_target(self) -> int | float:
        """
        calculate the distance between the end effector
        and the target
        """
        dist, _ = trig(self.segments[-1].end, self.target)
        return dist
    
    def distance_root_to_target(self) -> int | float:
        """
        calculate the distance between the end effector
        and the target
        """
        dist, _ = trig(self.segments[0].start, self.target)
        return dist

    def angle_to_target(self) -> int | float:
        """
        calculate the angle between the end effector
        and the target
        """
        _, angle = trig(self.segments[-1].end, self.target)
        return angle

    def forward_kinematics(self):
        """
        perform forward kinematics
        """
        for segment in self.segments:
            segment.calculate_start()
            segment.calculate_end()

    def draw_all_segments(self, camera):
        for segment in self.segments:
            segment.draw(camera)

    def draw_root(self, camera):
        pygame.draw.circle(camera.display, (0, 255, 0), self.segments[0].start, 10)


    def direction(self, segment: Segment, sample_distance: int | float = 0.1) -> int:
        """
        determines which direction changing the angle of a given segment
        minimizes the distance between the end effector and the target

        Arguments
        ---------
        arm (Arm)
        the radius of the arm's maximum reach
        segment (Segment)
        the segment in question
        sample_distance (int|float)
        how much to 'wiggle' each angle to determine
        which direction it shuold be moved

        Returns
        -------
        (int)
        the sign of the angle change (or 0 if no change needed)
        """
        distance_1 = self.distance_to_target()
        segment.angle += sample_distance
        self.forward_kinematics()

        distance_2 = self.distance_to_target()
        segment.angle -= sample_distance  # reset angle
        self.forward_kinematics()

        if distance_2 == distance_1:
            return 0
        if distance_2 < distance_1:
            return 1
        return -1


    def ccd(self, lr: int | float = 0.1, h: int | float = 0.5) -> None:
        """
        performs cyclic coordinate descent, a recursive implementation
        of Euler's method that moves each joint towards the solution

        Arguments
        ---------
        arm (Arm)
            the arm we are trying to update
        lr (int | float)
            the "learning rate", or how fast the arm converges to a target.
            Defaults to 0.1
        h (int | float)
            the step size, to standardize updates for different timesteps.
            Defaults to 0.1

        Returns
        -------
        None

        Side Effects
        ------------
        Changes the angle of each joint in the given arm following the CCD algorithm
        """
        # 1. calculate the distance between the end effector and the target
        # 2. calculate the direction in which the segment should move
        # 3. update the angle of the given segment
        # 4. recompute the forward kinematics of the arm
        # 5. repeat 1-4 for each segment

        # NOTE: only performs once per timestep

        for segment in self.segments:
            segment.angle += h * lr * self.distance_to_target() * self.direction(segment)
            self.forward_kinematics()

    def update(self, camera):

        # move towards target
        self.ccd()

        # perform forward kinematics
        self.forward_kinematics()

        # draw all segments
        self.draw_all_segments(camera)

        # draw root
        self.draw_root(camera)

