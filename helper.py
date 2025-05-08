from enum import Enum
import pygame
import random
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

# make the direction class with 4 directions
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

def direction_one_hot(direction):
    if direction == Direction.RIGHT:
        return [1, 0, 0, 0]
    elif direction == Direction.LEFT:
        return [0, 1, 0, 0]
    elif direction == Direction.UP:
        return [0, 0, 1, 0]
    elif direction == Direction.DOWN:
        return [0, 0, 0, 1]

# this will just represent where the snake is right now
Point = namedtuple('Point', 'x, y')

# constantsa
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
BLACK = (0,0,0)

BOARD_DIM = 6
BLOCK_SIZE = int(480/BOARD_DIM)
SPEED = 40
WIDTH = 480
HEIGHT = 480