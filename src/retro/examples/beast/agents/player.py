from retro.examples.beast.helpers import add, get_occupant

direction_vectors = {
    "KEY_RIGHT": (1, 0),
    "KEY_UP": (0, -1),
    "KEY_LEFT": (-1, 0),
    "KEY_DOWN": (0, 1),
}

class Player:
    character = "*"
    color = "white"
    name = "player"

    def __init__(self, position):
        self.position = position

    def handle_keystroke(self, keystroke, game):
        if keystroke.name in direction_vectors:
            vector = direction_vectors[keystroke.name]
            self.try_to_move(vector, game)

    def try_to_move(self, vector, game):
        """Tries to move the player in the direction of vector.
        If the space is empty and it's on the board, then the move succeeds. 
        If the space is occupied, then if the occupant can be pushed, it gets
        pushed and the move succeeds. Otherwise, the move fails. 
        """
        future_position = add(self.position, vector)
        on_board = game.on_board(future_position)
        obstacle = get_occupant(game, future_position)
        if obstacle:
            if obstacle.deadly:
                self.die(game)
            elif obstacle.handle_push(vector, game):
                self.position = future_position
        elif on_board:
            self.position = future_position

    def die(self, game):
        self.color = "black_on_red"
        game.state["message"] = "The beasties win!"
        game.end()

