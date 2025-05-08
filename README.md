# improved_DQN_snake

this will be an implemenation of the snake game, with some algorithms implemented on top of the snake game.

the snake game is relatively simple, and we will record all the records including moves, states, and rewards after every move. The board that we will be playing on is 6x6, for simplicity

The state of the game after every move will be quite a bit complicated, which is why I wanted to keep the size of the board kind of small for now. 
The state includes the following:
- a matrix representing the board with the position of the snake
- a matrix representing the board with the position of the snake head
- a matrix representing the board with the position of the food
- a danger flag to show if the snake will collide in each of the four immediate directions
- a food direction flag which indices which direction the food is in
- the direction that the snake is currently going

this means that in total, each state will be a vector with 119 values

The Snake game build itself will be relatively simple, with the following functions:
- **`__init__`**: sets up the game window, snake, food, and initializes game state  
- **`reset`**: resets the game to the starting state for a new episode  
- **`_place_food`**: places food randomly on the grid, avoiding the snake's body  
- **`play_step`**: processes a single step of the game (movement, reward, game over)  
- **`is_collision`**: checks if the snake hits a wall or itself  
- **`_update_ui`**: draws the snake, food, and score on the Pygame window  
- **`_move`**: updates the snake's direction and moves the head based on the action  
- **`get_danger_flags`**: returns whether straight, left, or right moves would cause a collision  
- **`get_food_direction`**: returns a vector indicating the direction of the food relative to the head  
- **`get_game_state`**: returns a flattened representation of the entire game state, combining the board layout, snake position, food, direction, danger flags, and food direction — used for learning or analysis.

For each step, the user/model can input one of 3 actions, represented as a one-hot vector: [1, 0, 0] to go straight, [0, 1, 0] to turn right, and [0, 0, 1] to turn left`, with the direction change being relative to the snake's current heading. 

For this experiment, the target policy will just be for the snake to keep going in the same direction if there is food in that direction, or to turn to one of the directions with the food. Since the food can be in more than one direction (for example, if the food was diagonal from the snake), the target policy will first tell the snake to keep going in the same direction, and then to turn only when necessary.