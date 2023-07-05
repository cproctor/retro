from retro.game import Game
from retro.agent import ArrowKeyAgent

game = Game([ArrowKeyAgent()], {}, debug=True)
game.play()

