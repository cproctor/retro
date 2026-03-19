class Goal:
    """The goal the player must reach to win."""
    character = "$"
    color = "yellow_on_black"

    def __init__(self, position):
        self.position = position

    def play_turn(self, game):
        """End the game when any other agent (the player) reaches this position."""
        agents_here = game.get_agents_by_position().get(self.position, [])
        if len(agents_here) > 1:
            game.end()
