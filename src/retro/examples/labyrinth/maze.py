from collections import defaultdict
import random


class Block:
    """A wall block. Stays in place and cannot be moved through."""
    character = "█"
    color = "white_on_black"
    solid = True

    def __init__(self, position):
        self.position = position


class Maze:
    """Generates a maze using a depth-first search algorithm.

    The maze is stored as a set of links (open passages) between room nodes.
    Room nodes sit at odd (x, y) coordinates; the cells between them (at even
    coordinates) are either walls or open corridors depending on whether the
    two adjacent rooms are linked.

    Args:
        columns: total board width, including outer walls.
        rows: total board height, including outer walls.
    """

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.links = defaultdict(set)
        self.generate()

    def generate(self, seed=None):
        """Generates a random perfect maze using iterative depth-first search.

        Every room is reachable and there is exactly one path between any two
        rooms. The algorithm works like a worm: it picks an unvisited neighbor,
        carves a passage to it, and moves there. When it gets stuck in a dead
        end, it backtracks along its history until it finds a room with
        unvisited neighbors. It finishes when the history stack is empty.

        Args:
            seed: Optional random seed. Pass the same seed to get the same maze.
        """
        if seed is not None:
            random.seed(seed)
        self.links = defaultdict(set)
        visited = set()
        current = (1, 1)
        stack = [current]
        while stack:
            visited.add(current)
            unvisited = [n for n in self.neighbors(current) if n not in visited]
            if unvisited:
                neighbor = random.choice(unvisited)
                self.connect(current, neighbor)
                stack.append(current)
                current = neighbor
            else:
                current = stack.pop()

    def connect(self, p0, p1):
        """Opens a passage between two adjacent room nodes."""
        self.links[p0].add(p1)
        self.links[p1].add(p0)

    def connected(self, p0, p1):
        """Returns True if there is an open passage between p0 and p1."""
        return p1 in self.links[p0]

    def neighbors(self, point):
        """Returns the room nodes two steps away in each cardinal direction."""
        x, y = point
        candidates = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        return [p for p in candidates if self.is_in_bounds(p)]

    def is_in_bounds(self, point):
        """Returns True if point is inside the outer wall boundary."""
        x, y = point
        return 0 < x < self.columns - 1 and 0 < y < self.rows - 1

    def get_walls(self):
        """Returns a list of (x, y) positions that should be walls.

        - Outer edge cells are always walls.
        - Interior cells where both coordinates are even are always walls
          (corner pillars between four rooms).
        - A cell with one even and one odd coordinate is a wall unless the two
          rooms on either side of it are linked.
        """
        walls = []
        for x in range(self.columns):
            for y in range(self.rows):
                if x == 0 or x == self.columns - 1 or y == 0 or y == self.rows - 1:
                    walls.append((x, y))
                elif x % 2 == 0 and y % 2 == 0:
                    walls.append((x, y))
                elif x % 2 == 0 and (x + 1, y) not in self.links[(x - 1, y)]:
                    walls.append((x, y))
                elif y % 2 == 0 and (x, y + 1) not in self.links[(x, y - 1)]:
                    walls.append((x, y))
        return walls

    def choose_start_and_end(self):
        """Returns (start, end) board positions for the player and the goal.

        The player starts at the top-left room; the goal is at the
        bottom-right room. Room nodes always sit at odd coordinates, so the
        end position is the largest odd x and y that are within the boundary.
        """
        start = (1, 1)
        end_x = self.columns - 2
        if end_x % 2 == 0:
            end_x -= 1
        end_y = self.rows - 2
        if end_y % 2 == 0:
            end_y -= 1
        return start, (end_x, end_y)

    def get_agents(self):
        """Returns a Block agent for every wall position in the maze."""
        return [Block(pos) for pos in self.get_walls()]
