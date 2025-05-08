import pygame
from game import SnakeGame
from agent import RandomAgent


if __name__ == '__main__':
    print("random agent")
    game = SnakeGame()
    agent = RandomAgent() 
    
    game.reset()

    running = True
    while running:
        action = agent.select_action()

    #     # Play one step
        reward, game_over, score = game.play_step(action)

    #     # Get current state (already relative, includes danger and food info)
    #     state = game.get_game_state()
    #     agent.store_transition(state, action, reward)

    #     print(f"Score: {score}")

    #     # End game if over
        if game_over:
            print("Game Over!")
            game.reset()

    #     # Update display
        game._update_ui()
        game.clock.tick(100)

    pygame.quit()
