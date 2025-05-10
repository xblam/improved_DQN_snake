from enum import Enum
import pygame
import random
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

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

BOARD_DIM = 10
BLOCK_SIZE = int(480/BOARD_DIM)
SPEED = 1000000
WIDTH = 480
HEIGHT = 480

# reward/penalties
FOOD_REWARD = 25
DEATH_PENALTY = -150
STEP_PENALTY = -1

# plotting helper

def plot_scores(scores, window=50, model = "DQN"):
    plt.figure(figsize=(10, 6))
    plt.plot(scores, label="scores per game")

    if len(scores) >= window:
        moving_avg = np.convolve(scores, np.ones(window)/window, mode='valid')
        plt.plot(range(window - 1, len(scores)), moving_avg, label=f"{window}-game average")

    plt.title(model + " Snake results")
    plt.xlabel("game")
    plt.ylabel("score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
