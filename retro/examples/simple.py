from retro.game import Game
from retro.agent import ArrowKeyAgent

agent = ArrowKeyAgent()
state = {}
game = Game([agent], state)
game.play()
