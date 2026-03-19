from retro.agent import ArrowKeyAgent, CenterViewAgent


class Player(ArrowKeyAgent, CenterViewAgent):
    """The player character. Use the arrow keys to navigate the maze.

    Inherits arrow-key movement from :py:class:`~retro.agent.ArrowKeyAgent`
    and automatic view-centering from :py:class:`~retro.agent.CenterViewAgent`.
    """
    character = "*"
    color = "red_on_black"
    margin = 5

    def __init__(self, position):
        self.position = position

    def try_to_move(self, position, game):
        """Move to position only if it is on the board and not blocked.

        A position is blocked if any agent there has ``solid = True``
        (which wall blocks do).
        """
        if game.on_board(position):
            agents_there = game.get_agents_by_position().get(position, [])
            if not any(getattr(a, 'solid', False) for a in agents_there):
                self.position = position
