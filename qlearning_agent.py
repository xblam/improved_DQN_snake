import random
import numpy as np
from collections import defaultdict
from helper import *

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(3))  # 3 actions
        self.last_state = None
        self.last_action = None

    def get_state(self, game):
        head = game.head

        def get_next_point(point, direction):
            if direction == Direction.RIGHT:
                return Point(point.x + BLOCK_SIZE, point.y)
            elif direction == Direction.LEFT:
                return Point(point.x - BLOCK_SIZE, point.y)
            elif direction == Direction.DOWN:
                return Point(point.x, point.y + BLOCK_SIZE)
            elif direction == Direction.UP:
                return Point(point.x, point.y - BLOCK_SIZE)

        dir_l = clockwise[(clockwise.index(game.direction) - 1) % 4]
        dir_r = clockwise[(clockwise.index(game.direction) + 1) % 4]
        dir_s = game.direction

        point_l = get_next_point(head, dir_l)
        point_r = get_next_point(head, dir_r)
        point_s = get_next_point(head, dir_s)

        state = (
            game.is_collision(point_s),  # danger ahead
            game.is_collision(point_r),  # danger right
            game.is_collision(point_l),  # danger left
            game.direction == Direction.LEFT,
            game.direction == Direction.RIGHT,
            game.direction == Direction.UP,
            game.direction == Direction.DOWN,
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y   # food down
        )
        return tuple(int(x) for x in state)


    def select_action(self, state):
        if random.random() < self.epsilon:
            action_idx = random.randint(0, 2)
        else:
            action_idx = np.argmax(self.q_table[state])
        action = [[1,0,0], [0,1,0], [0,0,1]][action_idx]
        self.last_state = state
        self.last_action = action_idx
        return action

    def store_state_transition(self, new_state, reward, done):
        old_q = self.q_table[self.last_state][self.last_action]
        next_max = 0 if done else np.max(self.q_table[new_state])
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.q_table[self.last_state][self.last_action] = new_q

    def reset_episode(self):
        self.last_state = None
        self.last_action = None