from retro.game import Game
from retro.examples.beast.board import Board

WIDTH = 40
HEIGHT = 20
NUM_BEASTS = 10

board = Board(WIDTH, HEIGHT, num_beasts=NUM_BEASTS)
state = {}
game = Game(board.get_agents(), state, board_size=(WIDTH, HEIGHT))
game.num_beasts = NUM_BEASTS
game.play()
