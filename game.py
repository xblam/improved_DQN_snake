from helper import *
from agent import RandomAgent
from qlearning_agent import QLearningAgent

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
        reward = STEP_PENALTY
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = DEATH_PENALTY
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = FOOD_REWARD
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    # check for collisions
    def is_collision(self, pt = None):
        if not pt:
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
