from random import randint
from retro.game import Game

class SnakeHead:
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    name = "Snake head"
    position = (0, 0)
    direction = DOWN
    character = 'v'
    next_segment = None
    growing = False

    def play_turn(self, game):
        x, y = self.position
        dx, dy = self.direction
        if self.can_move((x+dx, y+dy), game):
            self.position = (x+dx, y+dy)
            if self.is_on_apple(self.position, game):
                apple = game.get_agent_by_name("Apple")
                apple.relocate(game)
                self.growing = True
            if self.next_segment:
                self.next_segment.move((x, y), game, growing=self.growing)
            elif self.growing:
                self.next_segment = SnakeBodySegment(1, (x, y))
                game.add_agent(self.next_segment)
                game.state['score'] += 1
            self.growing = False

    def handle_keystroke(self, keystroke, game):
        x, y = self.position
        if keystroke.name == "KEY_RIGHT":
            self.direction = self.RIGHT
            self.character = '>'
        elif keystroke.name == "KEY_UP":
            self.direction = self.UP
            self.character = '^'
        elif keystroke.name == "KEY_LEFT":
            self.direction = self.LEFT
            self.character = '<'
        elif keystroke.name == "KEY_DOWN":
            self.direction = self.DOWN
            self.character = 'v'

    def can_move(self, position, game):
        on_board = game.on_board(position)
        empty = game.is_empty(position)
        on_apple = self.is_on_apple(position, game)
        return on_board and (empty or on_apple)

    def is_on_apple(self, position, game):
        apple = game.get_agent_by_name("Apple")
        return apple.position == position

class SnakeBodySegment:
    character = '*'
    next_segment = None

    def __init__(self, segment_id, position):
        self.segment_id = segment_id
        self.name = f"Snake body segment {segment_id}"
        self.position = position

    def move(self, new_position, game, growing=False):
        old_position = self.position
        self.position = new_position
        if self.next_segment:
            self.next_segment.move(old_position, game, growing=growing)
        elif growing:
            self.next_segment = SnakeBodySegment(self.segment_id + 1, old_position)
            game.add_agent(self.next_segment)
            game.state['score'] += self.segment_id + 1

class Apple:
    name = "Apple"
    character = '@'
    position = (0, 0)

    def relocate(self, game):
        self.position = self.random_empty_position(game)

    def random_empty_position(self, game):
        bw, bh = game.board_size
        occupied_positions = game.get_agents_by_position()
        while True:
            position = (randint(0, bw-1), randint(0, bh-1))
            if position not in occupied_positions:
                return position

if __name__ == '__main__':
    head = SnakeHead()
    apple = Apple()
    game = Game([head, apple], {'score': 0}, board_size=(32, 16))
    apple.relocate(game)
    game.play()

