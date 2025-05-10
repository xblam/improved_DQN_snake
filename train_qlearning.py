import pygame
from game import SnakeGame
from qlearning_agent import QLearningAgent
from helper import plot_scores

def train_qlearning(n_games=1000, print_log = True):
    game = SnakeGame()
    agent = QLearningAgent()
    # agent = game.agent
    scores = []
    recent_scores = []

    for episode in range(n_games):
        game.reset()
        total_reward = 0
        done = False
        state = agent.get_state(game)

        while not done:
            action = agent.select_action(state)
            reward, done, score = game.play_step(action)
            new_state = agent.get_state(game)
            agent.store_state_transition(new_state, reward, done)
            state = new_state
            total_reward += reward

        agent.reset_episode()
        scores.append(score)
        recent_scores.append(score)
        
        if print_log == 2:
            print(f"Game {episode+1}, Score: {score}, Total Reward: {total_reward}")
            
        if (episode + 1) % 10 == 0:
            if print_log > 1:
                print("Last 10 Scores:", recent_scores)
                recent_scores = []

    plot_scores(scores, window = 50, model = "Q-Learning")

    print("Done Training")
    pygame.quit()

if __name__ == '__main__':
    train_qlearning(n_games = 1000, print_log = 2)