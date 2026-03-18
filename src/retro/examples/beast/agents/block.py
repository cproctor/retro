from retro.examples.beast.helpers import add, get_occupant

class Block:
    """Represents a static block. It just sits there.
    """
    character = "█"
    color = "green4"
    deadly = False

    def __init__(self, position):
        self.position = position

    def handle_push(self, vector, game):
        """Responds to a push in the direction of vector. 
        Returns True when the push succeeds in creating
        empty space.
        """
        future_position = add(self.position, vector)
        on_board = game.on_board(future_position)
        obstacle = get_occupant(game, future_position)
        if obstacle:
            success = obstacle.handle_push(vector, game)
        else:
            success = on_board
        if success:
            self.position = future_position
        return success
