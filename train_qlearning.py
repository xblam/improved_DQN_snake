import pygame
from game import SnakeGame
from qlearning_agent import QLearningAgent

def train_qlearning(n_games=1000):
    game = SnakeGame()
    agent = QLearningAgent()
    # agent = game.agent
    scores = []

    for episode in range(n_games):
        game.reset()
        total_reward = 0
        done = False
        state = agent.get_state(game)

        while not done:
            action = agent.select_action(state)
            reward, done, score = game.play_step(action)
            new_state = agent.get_state(game)
            agent.store_transition(new_state, reward, done)
            state = new_state
            total_reward += reward

        agent.reset_episode()
        scores.append(score)
        print(f"Game {episode+1}, Score: {score}, Total Reward: {total_reward}")

    pygame.quit()

if __name__ == '__main__':
    train_qlearning(n_games=500)