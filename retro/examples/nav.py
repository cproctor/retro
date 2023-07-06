from random import randint
from retro.game import Game

HEIGHT = 25
WIDTH = 25

class Spaceship:
    """A player-controlled agent which moves left and right, dodging asteroids.
    Spaceship is a pretty simple class. The ship's character is ``^``, and 
    its position starts at the bottom center of the screen. 
    """
    name = "ship"
    character = '^'
    position = (WIDTH // 2, HEIGHT - 1)
    color = "black_on_skyblue1"

    def handle_keystroke(self, keystroke, game):
        """When the 
        left or arrow key is pressed, it moves left or right. If the ship's 
        new position is empty, it moves to that position. If the new position 
        is occupied (by an asteroid!) the game ends. 
        """
        x, y = self.position
        if keystroke.name in ("KEY_LEFT", "KEY_RIGHT"):
            if keystroke.name == "KEY_LEFT": 
                new_position = (x - 1, y)
            else: 
                new_position = (x + 1, y)
            if game.on_board(new_position):
                if game.is_empty(new_position):
                    self.position = new_position
                else:
                    self.explode()
                    game.end()

    def explode(self):
        """Sets the ship's character to ``*`` and its color to red.
        """
        self.color = "crimson_on_skyblue1"
        self.character = '*'

class Asteroid:
    """When Asteroids are spawned, they fall down the screen until they
    reach the bottom row and are removed. 
    An Asteroid's position is set when it is created.
    Whenever an asteroid moves, it 
    checks whether it has it the ship. 
    """
    character = 'O'
    color = "deepskyblue1_on_skyblue1"

    def __init__(self, position):
        self.position = position

    def play_turn(self, game):
        """Nothing happens unless
        ``game.turn_number`` is divisible by 2. The result is that asteroids 
        only move on even-numbered turns. If the asteroid is at the bottom of 
        the screen, it has run its course and should be removed from the game. 
        Otherwise, the asteroid's new position is one space down from its old 
        position. If the asteroid's new position is the same as the ship's 
        position, the game ends. 
        """
        if game.turn_number % 2 == 0: 
            self.set_color()
            x, y = self.position
            if y == HEIGHT - 1: 
                game.remove_agent(self)
            else:
                ship = game.get_agent_by_name('ship')
                new_position = (x, y + 1)
                if new_position == ship.position:
                    ship.explode()
                    game.end()
                else:
                    self.position = new_position

    def set_color(self):
        """To add to the game's drama, asteroids gradually become visible as they
        fall down the screen. This method calculates the ratio of the asteroid's 
        position compared to the screen height--0 is the top of the screen and 1 is
        the bottom ot the screen. Then sets the asteroid's color depending on the
        ratio. (`Available colors <https://blessed.readthedocs.io/en/latest/colors.html>`_)
        """
        x, y = self.position
        ratio = y / HEIGHT
        if ratio < 0.2: 
            self.color = "deepskyblue1_on_skyblue1"
        elif ratio < 0.4: 
            self.color = "deepskyblue2_on_skyblue1"
        elif ratio < 0.6:
            self.color = "deepskyblue3_on_skyblue1"
        else:
            self.color = "deepskyblue4_on_skyblue1"

class AsteroidSpawner:
    """An agent which is not displayed on the board, but which constantly spawns
    asteroids.
    """
    display = False

    def play_turn(self, game):
        """Adds 1 to the game score and then uses 
        :py:meth:`~retro.examples.nav.should_spawn_asteroid` to decide whether to 
        spawn an asteroid. When :py:meth:`~retro.examples.nav.should_spawn_asteroid` 
        comes back ``True``, creates a new instance of 
        :py:class:`~retro.examples.nav.Asteroid` at a random position along the 
        top of the screen and adds the asteroid to the game. 
        """
        game.state['score'] += 1
        if self.should_spawn_asteroid(game.turn_number):
            asteroid = Asteroid((randint(0, WIDTH - 1), 0))
            game.add_agent(asteroid)

    def should_spawn_asteroid(self, turn_number):
        """Decides whether to spawn an asteroid.
        Uses a simple but effective algorithm to make the game get
        progressively more difficult: choose a random number and return 
        ``True`` if the number is less than the current turn number. At 
        the beginning of the game, few asteroids will be spawned. As the 
        turn number climbs toward 1000, asteroids are spawned almost 
        every turn. 

        Arguments:
            turn_number (int): The current turn in the game.
        """
        return randint(0, 1000) < turn_number

if __name__ == '__main__':
    ship = Spaceship()
    spawner = AsteroidSpawner()
    game = Game(
        [ship, spawner],
        {"score": 0},
        board_size=(WIDTH, HEIGHT),
        color="deepskyblue4_on_skyblue1",
    )
    game.play()

