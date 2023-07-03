class Agent:
    name = "Agent"
    character = "*"
    position = (0,0)
    display = True
    z = 0

    def play_turn(self, game):
        pass

    def handle_keystroke(self, keystroke, game):
        x, y = self.position
        if keystroke.name == "KEY_RIGHT":
            self.try_to_move(x + 1, y, game)
        elif keystroke.name == "KEY_UP":
            self.try_to_move(x, y - 1, game)
        elif keystroke.name == "KEY_LEFT":
            self.try_to_move(x - 1, y, game)
        elif keystroke.name == "KEY_DOWN":
            self.try_to_move(x, y + 1, game)

    def try_to_move(self, x, y, game):
        if game.on_board((x, y)):
            self.position = (x, y)
