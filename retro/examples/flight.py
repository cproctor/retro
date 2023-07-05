from random import randint
from retro.game import Game

HEIGHT = 25
WIDTH = 25

class Spaceship:
    name = "ship"
    character = '^'
    position = (WIDTH // 2, HEIGHT - 1)
    color = "black_on_skyblue1"

    def handle_keystroke(self, keystroke, game):
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
        self.color = "crimson_on_skyblue1"
        self.character = '*'

class Asteroid:
    character = 'O'
    color = "deepskyblue1_on_skyblue1"

    def __init__(self, name, position):
        self.name = name
        self.position = position

    def play_turn(self, game):
        if game.turn_number % 2 == 0: 
            self.set_color()
            x, y = self.position
            if y == HEIGHT - 1: 
                game.remove_agent_by_name(self.name)
            else:
                ship = game.get_agent_by_name('ship')
                new_position = (x, y + 1)
                if new_position == ship.position:
                    ship.explode()
                    game.end()
                else:
                    self.position = new_position

    def set_color(self):
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
    name = "spawner"
    character = 'x'
    display = False

    def play_turn(self, game):
        game.state['score'] += 1
        if self.should_spawn_asteroid(game.turn_number):
            asteroid = Asteroid(
                f"asteroid {game.turn_number}",
                (randint(0, WIDTH - 1), 0)
            )
            game.add_agent(asteroid)

    def should_spawn_asteroid(self, turn_number):
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

