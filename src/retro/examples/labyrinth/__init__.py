from retro.game import Game
from retro.examples.labyrinth.goal import Goal
from retro.examples.labyrinth.maze import Maze
from retro.examples.labyrinth.player import Player

WIDTH = 400
HEIGHT = 200
VIEW_WIDTH = 40
VIEW_HEIGHT = 20


class ScoreKeeper:
    """Counts down the score by 1 each second. Not displayed on the board."""
    display = False

    def play_turn(self, game):
        if game.turn_number % game.framerate == 0:
            game.state['score'] -= 1


state = {"score": 500}
maze = Maze(WIDTH, HEIGHT)
start, end = maze.choose_start_and_end()
player = Player(start)
goal = Goal(end)
game = Game(
    [player, goal, ScoreKeeper()] + maze.get_agents(),
    state,
    board_size=(WIDTH, HEIGHT),
    view_size=(VIEW_WIDTH, VIEW_HEIGHT),
    wait_for_enter=True,
)
player.center_view(game)
game.play()
