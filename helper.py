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

clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]


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