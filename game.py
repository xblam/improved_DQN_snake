from helper import *
from agent import RandomAgent

class SnakeGame:
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    # reset the game
    def reset(self):
        self.direction = Direction.UP
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                    Point(self.head.x-BLOCK_SIZE, self.head.y),
                    Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0



    # put down food
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    # move the snake
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    # check for collisions
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    # update the pygame window
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    # move the snake
    def _move(self, action):
        # [straight, right, left]

        idx = clockwise.index(self.direction)

        # no change, turn right, and turn left respectively
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clockwise[next_idx]
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clockwise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


    def closest_obstacle(self, direction):
        x, y = int(self.head.x), int(self.head.y)
        distance = 0

        while True:
            if direction == Direction.RIGHT:
                x += BLOCK_SIZE
            elif direction == Direction.LEFT:
                x -= BLOCK_SIZE
            elif direction == Direction.UP:
                y -= BLOCK_SIZE
            elif direction == Direction.DOWN:
                y += BLOCK_SIZE

            distance += 1

            # check for wall
            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                break

            # check for snake body
            if Point(x, y) in self.snake[1:]:
                break

        return distance  # number of steps before obstacle


    # to see if any of the possible directions result in instant death
    def get_danger_flags(self):
        head = self.head
        dir = self.direction

        # Clockwise directions: RIGHT → DOWN → LEFT → UP
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(dir)

        # Calculate directions relative to current heading
        dir_straight = clockwise[idx]
        dir_right = clockwise[(idx + 1) % 4]
        dir_left = clockwise[(idx - 1) % 4]

        # Use self.is_collision to check danger
        danger_straight = self.closest_obstacle(dir_straight)
        danger_right   = self.closest_obstacle(dir_right)
        danger_left    = self.closest_obstacle(dir_left)

        return [danger_straight, danger_right, danger_left]
   
    def get_game_state(self):
        rows = self.h // BLOCK_SIZE
        cols = self.w // BLOCK_SIZE

        snake_matrix = np.zeros((rows, cols), dtype=int)
        snake_head_matrix = np.zeros((rows, cols), dtype=int)
        food_matrix = np.zeros((rows, cols), dtype=int)

        fx, fy = int(self.food.x // BLOCK_SIZE), int(self.food.y // BLOCK_SIZE)
        food_matrix[fy][fx] = 1

        for segment in self.snake[1:]:
            x, y = int(segment.x // BLOCK_SIZE), int(segment.y // BLOCK_SIZE)
            snake_matrix[y][x] = 1

        hx, hy = int(self.head.x // BLOCK_SIZE), int(self.head.y // BLOCK_SIZE)
        snake_head_matrix[hy][hx] = 1

        # Combine matrices and relative indicators
        state = np.concatenate((
            snake_matrix.flatten(),
            snake_head_matrix.flatten(),
            food_matrix.flatten(),
            self.get_danger_flags(),           # [danger_straight, right, left]
            self.get_relative_food_direction() # [food_ahead, right, left]
        ))

        print(state.shape)
        print(state)
        return state


# RUN THE SNAKE MANUALLY -----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    game = SnakeGame()
    game.reset()

    running = True
    action = [1, 0, 0]  # default: go straight

    while running:
        print(game.get_danger_flags())
        event_happened = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                event_happened = True
                if event.key == pygame.K_LEFT:
                    action = [0, 0, 1]  # turn left
                elif event.key == pygame.K_RIGHT:
                    action = [0, 1, 0]  # turn right
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    action = [1, 0, 0]  # go straight

        if event_happened:
            reward, game_over, score = game.play_step(action)
            print("Score:", score)

            if game_over:
                print("Game Over! Final score:", score)
                pygame.time.delay(1000)
                game.reset()
                action = [1, 0, 0]


        game._update_ui()
        game.clock.tick(30)  # Higher value = more responsive UI, not snake speed


# LET THE RANDOM AGENT PLAY THE GAME -----------------------------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     game = SnakeGame()
#     agent = RandomAgent() 
    
#     game.reset()

#     running = True
#     while running:
#         print(game.get_danger_flags())
#         action = agent.select_action()

#     #     # Play one step
#         reward, game_over, score = game.play_step(action)

#     #     # Get current state (already relative, includes danger and food info)
#     #     state = game.get_game_state()
#     #     agent.store_transition(state, action, reward)

#     #     print(f"Score: {score}")

#     #     # End game if over
#         if game_over:
#             print("Game Over!")
#             game.reset()

#     #     # Update display
#         game._update_ui()
#         game.clock.tick(100)

#     pygame.quit()