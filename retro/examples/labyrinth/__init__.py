from retro.game import Game
from retro.examples.labyrinth.maze import Maze
from retro.examples.labyrinth.player import Player

WIDTH = 400
HEIGHT = 200
VIEW_WIDTH = 40
VIEW_HEIGHT = 20

state = {}
maze = Maze(WIDTH, HEIGHT)
start, end = maze.choose_start_and_end()
player = Player(start)
goal = Goal(end)
game = Game(
    [player] + maze.get_agents(), 
    state, 
    board_size=(WIDTH, HEIGHT), 
    view_size=(VIEW_WIDTH, VIEW_HEIGHT),
)
player.center_view(game)
game.play()
