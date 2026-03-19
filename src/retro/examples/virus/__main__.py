from retro.game import Game
from retro.examples.virus.token import Token

size = 12
initial_tokens = [
    Token((0, 0), first_player=True),
    Token((size-1, size-1), first_player=False),
]
game = Game(initial_tokens, {}, (size, size))
game.play()
