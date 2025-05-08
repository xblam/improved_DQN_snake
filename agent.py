from helper import *

class RandomAgent:
    def __init__(self):
        self.trajectory = []

    def select_action(self):
        # Randomly choose between straight, right, or left
        return random.choice([
            [1, 0, 0],  # go straight
            [0, 1, 0],  # turn right
            [0, 0, 1],  # turn left
        ])

    def store_transition(self, state, action, reward):
        self.trajectory.append((state, action, reward))

    def reset_episode(self):
        self.trajectory.clear()

def greedy_toward_food(game):
    direction = game.direction
    head = game.head
    food = game.food

    dx = food.x - head.x
    dy = food.y - head.y

    idx = clockwise.index(direction)

    # Check straight, right, left
    action_straight = [1, 0, 0]
    action_right = [0, 1, 0]
    action_left = [0, 0, 1]

    # Prefer moving toward food on x or y axis
    if direction in [Direction.RIGHT, Direction.LEFT]:
        if dy < 0:
            return action_left if direction == Direction.RIGHT else action_right
        elif dy > 0:
            return action_right if direction == Direction.RIGHT else action_left
    else:  # UP or DOWN
        if dx < 0:
            return action_right if direction == Direction.UP else action_left
        elif dx > 0:
            return action_left if direction == Direction.UP else action_right

    # If no clear better choice, go straight
    return action_straight
