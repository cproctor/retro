from retro.game import Game
from retro.examples.beast.board import Board

WIDTH = 40
HEIGHT = 20
NUM_BEASTS = 10

def create_game():
    """Return a fresh, initialized Beast game."""
    board = Board(WIDTH, HEIGHT, num_beasts=NUM_BEASTS)
    state = {'score': 0}
    game = Game(board.get_agents(), state, board_size=(WIDTH, HEIGHT))
    game.num_beasts = NUM_BEASTS
    return game

if __name__ == '__main__':
    create_game().play()
