.. _nav_v1:

Nav (Version 1)
===============

::

    from retro.game import Game

    HEIGHT = 25
    WIDTH = 25

    class Spaceship:
        name = "ship"
        character = '^'
        position = (WIDTH // 2, HEIGHT - 1)

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
                        game.end()

    class Asteroid:
        character = 'O'
    
        def __init__(self, position):
            self.position = position
    
        def play_turn(self, game):
            if game.turn_number % 2 == 0: 
                x, y = self.position
                if y == HEIGHT - 1: 
                    game.remove_agent_by_name(self.name)
                else:
                    ship = game.get_agent_by_name('ship')
                    new_position = (x, y + 1)
                    if new_position == ship.position:
                        game.end()
                    else:
                        self.position = new_position

    ship = Spaceship()
    asteroid = Asteroid("asteroid", (WIDTH // 2, 0))
    game = Game(
        [ship, asteroid], 
        {"score": 0}, 
        board_size=(WIDTH, HEIGHT)
    )
    game.play()
