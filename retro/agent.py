class Agent:
    name = "Agent"
    character = "*"
    position = (0,0)
    display = True
    z = 0

    def play_turn(self, game):
        x, y = self.position
        if game.on_board((x+1, y)):
            self.position = (x+1, y)

    def handle_keystroke(self, keystroke, game):
        pass
