from helper import *

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
        # just update the position of head
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

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

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

        def next_point(direction):
            x, y = head.x, head.y
            if direction == Direction.RIGHT:
                x += BLOCK_SIZE
            elif direction == Direction.LEFT:
                x -= BLOCK_SIZE
            elif direction == Direction.UP:
                y -= BLOCK_SIZE
            elif direction == Direction.DOWN:
                y += BLOCK_SIZE
            return Point(x, y)

        # Use self.is_collision to check danger
        danger_straight = 1 if self.is_collision(next_point(dir_straight)) else 0
        danger_right   = 1 if self.is_collision(next_point(dir_right)) else 0
        danger_left    = 1 if self.is_collision(next_point(dir_left)) else 0

        return [danger_straight, danger_right, danger_left]
   
    
    # get the game state
    def get_game_state(self):
        rows = self.h // BLOCK_SIZE
        cols = self.w // BLOCK_SIZE

        snake_matrix = np.zeros((rows, cols), dtype=int)
        snake_head_matrix = np.zeros((rows, cols), dtype=int)
        food_matrix = np.zeros((rows, cols), dtype=int)

        fx, fy = int(self.food.x // BLOCK_SIZE), int(self.food.y // BLOCK_SIZE)
        food_matrix[fy][fx] = 1

        # Snake body = 1
        for segment in self.snake[1:]:
            x, y = int(segment.x // BLOCK_SIZE), int(segment.y // BLOCK_SIZE)
            snake_matrix[y][x] = 1

        # Snake head = 2
        hx, hy = int(self.head.x // BLOCK_SIZE), int(self.head.y // BLOCK_SIZE)
        snake_head_matrix[hy][hx] = 1

        # combine all the matrices
        state = np.concatenate((
            snake_matrix.flatten(),
            snake_head_matrix.flatten(),
            food_matrix.flatten(),
            direction_one_hot(self.direction),
            self.get_danger_flags()
        ))
        print(state.shape)
        print(state)
        return state

class RandomAgent:
    def __init__(self):
        self.trajectory = []  # stores (state, action, reward)
        self.score = 0

    def select_action(self):
        return random.choice([
            [1, 0, 0],  # straight
            [0, 1, 0],  # right
            [0, 0, 1],  # left
        ])

    def store_transition(self, state, action, reward):
        self.trajectory.append((state, action, reward))

    def reset_episode(self):
        self.trajectory = []
        self.score = 0


if __name__ == '__main__':
    game = SnakeGame()
    game.reset()

    running = True
    while running:
        action = [1, 0, 0]  # default = go straight

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Determine action based on relative movement
                if event.key == pygame.K_LEFT:
                    action = [0, 0, 1]  # turn left
                elif event.key == pygame.K_RIGHT:
                    action = [0, 1, 0]  # turn right
                else:
                    action = [1, 0, 0]  # go straight (e.g., any other key)

                # Take one step in the game
                reward, game_over, score = game.play_step(action)
                print("Score:", score)
                game.get_game_state()  # for debugging or feeding into model

                if game_over:
                    print("Game Over!")
                    running = False

        game._update_ui()
        game.get_game_state()  # for debugging or feeding into model
        game.clock.tick(10)

    pygame.quit()


