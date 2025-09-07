import math
import pygame

'''
Useful functions for the future:
1) Normalization
2) 
'''

def distance(e1, e2):
    return math.hypot(e2[0]-e1[0], e2[1]-e1[1])

def angle(e1, e2):
    return math.atan2(e2[1]-e1[1], e2[0]-e1[0])

def trig(p1: pygame.Vector2 | tuple | list,
         p2: pygame.Vector2 | tuple | list) -> tuple[float, float]:
    """
    calculates the distance and angle (in radians)
    from p1 to p2

    Arguments
    ---------
    p1 (pygame.Vector2|tuple|list)
      the start position
    p2 (pygame.Vector2|tuple|list)
      the end position

    Returns
    -------
    (dist, angle) (tuple)
      the distance and angle from p1 to p2
    """
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]

    dist = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)

    return (dist, angle)


def polar_to_cartesian(start: pygame.Vector2 | tuple | list, angle: int | float,
                       length: int | float) -> pygame.Vector2:
    """
    finds the coordinates of the end point of a vector
    given a start position, angle, and length

    Arguments
    ---------
    start (pygame.Vector2|tuple|list)
      the vector's start position
    angle (int|float)
      the angle of the vector in radians
    length (int|float)
      the length of the vector

    Returns
    -------
    end (pygame.Vector2)
      the vector's endpoint
    """
    vector = pygame.Vector2()
    vector.from_polar((length, angle))

    return start + vector

def advance(vec, angle, amt):
    vec[0] += math.cos(angle) * amt
    vec[1] += math.sin(angle) * amt
    return vec

def sign(n):
    '''
    returns the sign (+/-) of a number
    '''
    if n == 0:
        return n
    return n/abs(n)
