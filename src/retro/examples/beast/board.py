from random import shuffle
from retro.examples.beast.agents.player import Player
from retro.examples.beast.agents.beast import Beast
from retro.examples.beast.agents.block import Block

class Board:
    """The Board creates the agents needed at the beginning of the game, 
    and assigns them all their positions. Board itself is not an agent, 
    and has no role once the game starts.
    """
    def __init__(self, width, height, block_density=0.3, num_beasts=10):
        self.width = width
        self.height = height
        self.block_density = block_density
        self.num_blocks = round(width * height * block_density)
        self.num_empty_spaces = width * height- self.num_blocks
        self.num_beasts = num_beasts
        self.validate()

    def validate(self):
        """Checks that the inputs are valid.
        """
        if self.block_density < 0 or self.block_density > 1:
            raise ValueError("block density must be between 0 and 1.")
        if self.num_empty_spaces < self.num_beasts + 1:
            raise ValueError("Not enough space on the board.")

    def get_agents(self):
        """Returns a list of agents, all initialized in their starting positions.
        """
        positions = self.get_all_positions()
        shuffle(positions)

        player_position = positions[0]
        beast_positions = positions[1:self.num_beasts + 1]
        block_positions = positions[-self.num_blocks:]

        player = [Player(player_position)]
        beasts = [Beast(pos) for pos in beast_positions]
        blocks = [Block(pos) for pos in block_positions]
        return player + beasts + blocks

    def get_all_positions(self):
        """Returns a list of all positions which are not on the edge of the board
        """
        positions = []
        for i in range(self.width):
            for j in range(self.height):
                positions.append((i, j))
        return positions
