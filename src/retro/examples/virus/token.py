class Token:
    """A token represents a piece on the board in the virus game. 
    Tokens never move. A token's character and color are determined
    by which player it belongs to and whether it is alive or dead. 
    """
    def __init__(self, position, first_player=True, alive=True):
        self.position = position
        self.first_player = first_player
        self.alive = alive
        self.set_appearance()

    def set_appearance(self):
        self.set_color()
        self.set_character()

    def set_color(self):
        if self.first_player: 
            self.color = "red"
        else:
            self.color = "blue"

    def set_character(self):
        if self.alive: 
            self.character = "O"
        else:
            self.character = "*"
