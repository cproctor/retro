from retro.examples.beast.helpers import add, distance, get_occupant
from random import random, choice

class Beast:
    """Represents a beast, coming after the player.
    """
    character = "H"
    color = "red"
    probability_of_moving = 0.03
    probability_of_random_move = 0.2
    deadly = True

    def __init__(self, position):
        self.position = position

    def handle_push(self, vector, game):
        future_position = add(self.position, vector)
        on_board = game.on_board(future_position)
        obstacle = get_occupant(game, future_position)
        if obstacle or not on_board:
            self.die(game)
            return True
        else:
            return False

    def play_turn(self, game):
        if self.should_move():
            possible_moves = []
            for position in self.get_adjacent_positions():
                if game.is_empty(position) and game.on_board(position):
                    possible_moves.append(position)
            if possible_moves:
                if self.should_move_randomly():
                    self.position = choice(possible_moves)
                else:
                    self.position = self.choose_best_move(possible_moves, game)
            player = game.get_agent_by_name("player")
            if player.position == self.position:
                player.die()

    def get_adjacent_positions(self):
        """Returns a list of all adjacent positions, including diagonals
        """
        positions = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i or j:
                    positions.append(add(self.position, (i, j)))
        return positions

    def should_move(self):
        return random() < self.probability_of_moving

    def should_move_randomly(self):
        return random() < self.probability_of_random_move

    def choose_best_move(self, possible_moves, game):
        player = game.get_agent_by_name("player")
        move_distances = [[distance(player.position, move), move] for move in possible_moves]
        shortest_distance, best_move = sorted(move_distances)[0]
        return best_move

    def die(self, game):
        game.remove_agent(self)
        game.num_beasts -= 1
        if game.num_beasts == 0:
            game.state["message"] = "You win!"
            game.end()
