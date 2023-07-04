from random import randint
from retro.game import Game

class Apple:
    """An agent representing the Apple. 
    Note how Apple doesn't have ``play_turn`` or 
    ``handle_keystroke`` methods: the Apple doesn't need to do 
    anything in this game. It just sits there waiting to get 
    eaten.

    Attributes:
        name: "Apple"
        character: '@'
        color: "red_on_black" (`Here's documentation on how colors 
            work <https://blessed.readthedocs.io/en/latest/colors.html>`_
        position: (0, 0). The Apple will choose a random position 
            as soon as the game starts, but it needs an initial 
            position to be assigned.

    """
    name = "Apple"
    character = '@'
    color = "red_on_black"
    position = (0, 0)

    def relocate(self, game):
        """Sets position to a random empty position. This method is 
        called whenever the snake's head touches the apple. 

        Arguments: 
            game (Game): The current game.
        """
        self.position = self.random_empty_position(game)

    def random_empty_position(self, game):
        """Returns a randomly-selected empty position. Uses a very 
        simple algorithm: Get the game's board size, choose a 
        random x-value between 0 and the board width, and choose 
        a random y-value between 0 and the board height. Now use 
        the game to check whether any Agents are occupying this 
        position. If so, keep randomly choosing a new position 
        until the position is empty.
        """
        bw, bh = game.board_size
        occupied_positions = game.get_agents_by_position()
        while True:
            position = (randint(0, bw-1), randint(0, bh-1))
            if position not in occupied_positions:
                return position

class SnakeHead:
    """An Agent representing the snake's head. When the game starts, you control
    the snake head using the arrow keys. The SnakeHead always has a direction, and 
    will keep moving in that direction every turn. When you press an arrow key, 
    you change the SnakeHead's direction. 

    Attributes:
        name: "Snake head"
        position: (0,0) 
        character: ``'v'`` Depending on the snake head's direction, its character
            changes to ``'<'``, ``'^'``, ``'>'``, or ``'v'``.
        next_segment: Initially ``None``, this is a reference to a SnakeBodySegment.
        growing: When set to True, the snake will grow a new segment on its next move.
    """
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
        """On each turn, the snake head uses its position and direction to figure out
        its next position. If the snake head is able to move there (it's on the board and 
        not occuppied by part of the snake's body), it moves. 

        Then, if the snake head is on the Apple, the Apple moves to a new random position
        and ``growing`` is set to True.

        Now we need to deal with two situations. First, if ``next_segment`` is not None, there is 
        a SnakeBodySegment attached to the head. We need the body to follow the head, 
        so we call ``self.next_segment.move``, passing the head's old position 
        (this will be the body's new position), a reference to the game, and a value for 
        ``growing``. If the snake needs to grow, we need to pass this information along
        the body until it reaches the tail--this is where the next segment will be attached. 

        If there is no ``next_segment`` but ``self.growing`` is True, it's time to add 
        a body! We set ``self.next_segment`` to a  new SnakeBodySegment, set its 
        position to the head's old position, and add it to the game. We also add 1 to the 
        game's score.
        """
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
        """Checks whether one of the arrow keys has been pressed. 
        If so, sets the SnakeHead's direction and character.
        """
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
    """Finally, we need an Agent for the snake's body segments. 
    SnakeBodySegment doesn't have ``play_turn`` or ``handle_keystroke`` methods because
    it never does anything on its own. It only moves when the SnakeHead, or the previous
    segment, tells it to move. 

    Arguments: 
        segment_id (int): Keeps track of how far back this segment is from the head.
            This is used to give the segment a unique name, and also to keep track 
            of how many points the player earns for eating the next apple. 
        position (int, int): The initial position.

    Attributes:
        character: '*'
        next_segment: Initially ``None``, this is a reference to a SnakeBodySegment
            when this segment is not the last one in the snake's body.
            
    """
    character = '*'
    next_segment = None

    def __init__(self, segment_id, position):
        self.segment_id = segment_id
        self.name = f"Snake body segment {segment_id}"
        self.position = position

    def move(self, new_position, game, growing=False):
        """When SnakeHead moves, it sets off a chain reaction, moving all its 
        body segments. Whenever the head or a body segment has another segment 
        (``next_segment``), it calls that segment's ``move`` method.

        This method updates the SnakeBodySegment's position. Then, if 
        ``self.next_segment`` is not None, calls that segment's ``move`` method. 
        If there is no next segment and ``growing`` is True, then we set
        ``self.next_segment`` to a new SnakeBodySegment in this segment's old
        position, and update the game's score.

        Arguments: 
            new_position (int, int): The new position.
            game (Game): A reference to the current game.
            growing (bool): (Default False) When True, the snake needs to 
                add a new segment. 
        """
        old_position = self.position
        self.position = new_position
        if self.next_segment:
            self.next_segment.move(old_position, game, growing=growing)
        elif growing:
            self.next_segment = SnakeBodySegment(self.segment_id + 1, old_position)
            game.add_agent(self.next_segment)
            game.state['score'] += self.segment_id + 1

if __name__ == '__main__':
    head = SnakeHead()
    apple = Apple()
    game = Game([head, apple], {'score': 0}, board_size=(32, 16), framerate=12)
    apple.relocate(game)
    game.play()

