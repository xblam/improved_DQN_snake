class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.thoughts = []
        self.actions = []
        self.tools = []
        self.tool_results = []
        self.tool_uses = []
        self.tool_use_results = []
        self.tool_use_thoughts = []
        self.tool_use_actions = []
        self.tool_use_tools = []
        self.tool_use_tool_results = []

def greedy_toward_food(game):
    direction = game.direction
    head = game.head
    food = game.food

    dx = food.x - head.x
    dy = food.y - head.y

    clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
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
