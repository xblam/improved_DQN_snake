import pygame
import numpy as np
from game import SnakeGame
from dqn_agent import DQNAgent
from helper import plot_scores

def train_dqn(n_games=1000, print_log=2):
    print("DQN")
    game = SnakeGame(obstacles=True)
    agent = DQNAgent()
    scores = []
    recent_scores = []

    for episode in range(n_games):
        game.reset()
        state = agent.get_state(game)
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)
            reward, done, score = game.play_step(action)
            next_state = agent.get_state(game)
            agent.store_transition(state, action, reward, next_state, done)
            agent.train_step()
            state = next_state
            total_reward += reward

        scores.append(score)
        recent_scores.append(score)

        if print_log == 2:
            print(f"Game {episode+1}, Score: {score}, Total Reward: {total_reward}")
            
        if (episode + 1) % 10 == 0:
            if print_log > 1:
                print("Last 10 Scores:", recent_scores)
                recent_scores = []

    plot_scores(scores, window=50)
    print("Done Training")
    pygame.quit()

if __name__ == '__main__':
    train_dqn(n_games=500, print_log=2)