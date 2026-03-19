from retro.agent import ArrowKeyAgent, CenterViewAgent

class Player(ArrowKeyAgent, CenterViewAgent):
    character = "*"
    color = "red_on_black"

    def __init__(self, position):
        self.position = position
