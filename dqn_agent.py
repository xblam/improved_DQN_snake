import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
from helper import *
from game import Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LinearQNet, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

class DQNAgent:
    def __init__(self, state_size=11, hidden_size=256, action_size=3):
        self.state_size = state_size
        self.action_size = action_size
        self.model = LinearQNet(state_size, hidden_size, action_size)
        self.target_model = LinearQNet(state_size, hidden_size, action_size)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()

        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()

        self.memory = deque(maxlen=MAX_MEMORY)
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.steps = 0
        self.update_target_every = 100

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
            game.is_collision(point_s),
            game.is_collision(point_r),
            game.is_collision(point_l),
            game.direction == Direction.LEFT,
            game.direction == Direction.RIGHT,
            game.direction == Direction.UP,
            game.direction == Direction.DOWN,
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y
        )
        return np.array(state, dtype=int)

    def select_action(self, state):
        self.steps += 1
        if random.random() < self.epsilon:
            move = random.randint(0, self.action_size - 1)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32)
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
        return [[1,0,0], [0,1,0], [0,0,1]][move]

    def store_transition(self, state, action, reward, next_state, done):
        action_index = [[1, 0, 0], [0, 1, 0], [0, 0, 1]].index(action)
        self.memory.append((state, action_index, reward, next_state, done))

    def train_step(self):
        if len(self.memory) < BATCH_SIZE:
            return

        mini_batch = random.sample(self.memory, BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*mini_batch)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        q_values = self.model(states)
        next_q_values = self.target_model(next_states)
        target_qs = q_values.clone()

        for i in range(BATCH_SIZE):
            max_next_q = torch.max(next_q_values[i]).item()
            target_q = rewards[i] + self.gamma * max_next_q * (not dones[i])
            target_qs[i][actions[i]] = target_q

        self.optimizer.zero_grad()
        loss = self.criterion(q_values, target_qs)
        loss.backward()
        self.optimizer.step()

        if self.steps % self.update_target_every == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay