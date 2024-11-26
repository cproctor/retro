from retro.agent import Tombstone
from retro.graph import Vertex, Edge, Graph
from retro.errors import TerminalTooSmall

identity = lambda x: x

def vector_add(vec0, vec1):
    "Adds two vectors."
    x0, y0 = vec0
    x1, y1 = vec1
    return (x0 + x1, y0 + y1)

class View:
    BORDER_X = 2
    BORDER_Y = 3
    STATE_HEIGHT = 5
    DEBUG_WIDTH = 60

    def __init__(self, terminal, color='white_on_black'):
        self.terminal = terminal
        self.terminal_size = (self.terminal.width, self.terminal.height)
        self.color = color
        self.initial_render = True

    def render(self, game):
        if self.initial_render or self.terminal_size_changed():
            self.terminal_size = (self.terminal.width, self.terminal.height)
            self.render_layout(game)
        if self.initial_render or game.state.changed:
            self.render_state(game)
        if game.debug:
            self.render_debug_log(game)
        prior_board = self.get_board(game.prior_agent_positions)
        board = self.get_board(game.agent_positions)
        diff = self.get_board_diff(prior_board, board)
        self.render_board(diff, game)
        self.initial_render = False

    def get_board(self, agent_positions):
        """Returns a dict of position -> colored_character.
        """
        board = {}
        for position, agents in agent_positions.items():
            top = sorted(agents, key=lambda a: getattr(a, 'z', 0), reverse=True)[0]
            if hasattr(top, 'color'):
                color = self.get_color(top.color)
            else:
                color = identity
            board[position] = color(top.character)
        return board

    def get_board_diff(self, board0, board1):
        """Returns a dict of position -> colored_character needed to transform
        board0 to board 1.
        """
        diff = {}
        positions = set(board0.keys()).union(board1.keys()) 
        for p in positions: 
            if p not in board0:
                diff[p] = board1[p]
            elif p not in board1:
                diff[p] = self.get_color(self.color)(' ')
            elif board0[p] != board1[p]:
                diff[p] = board1[p]
        return diff

    def render_board(self, board, game):
        origin = self.get_board_origin_coords(game)
        for position, colored_character in board.items():
            x, y = vector_add(origin, position)
            print(self.terminal.move_xy(x, y) + colored_character)

    def render_layout(self, game):
        bw, bh = game.board_size
        self.check_terminal_size(game)
        self.clear_screen()
        layout_graph = self.get_layout_graph(game)
        layout_graph.render(self.terminal)

    def clear_screen(self):
        print(self.terminal.home + self.get_color(self.color) + self.terminal.clear)

    def get_color(self, color_string):
        if not hasattr(self.terminal, color_string):
            msg = (
                f"{color_string} is not a supported color."
                "See https://blessed.readthedocs.io/en/latest/colors.html"
            )
            raise ValueError(msg)
        return getattr(self.terminal, color_string)

    def render_state(self, game):
        bw, bh = game.board_size
        ox, oy = self.get_state_origin_coords(game)
        color = self.get_color(self.color)
        for i, key in enumerate(sorted(game.state.keys())):
            msg = f"{key}: {game.state[key]}"[:bw]
            print(self.terminal.move_xy(ox, oy + i) + color(msg))

    def render_debug_log(self, game):
        bw, bh = game.board_size
        debug_height = bh + self.STATE_HEIGHT 
        ox, oy = self.get_debug_origin_coords(game)
        for i, (turn_number, message) in enumerate(game.log_messages[-debug_height:]):
            msg = f"{turn_number}. {message}"[:self.DEBUG_WIDTH - 1].ljust(self.DEBUG_WIDTH - 1)
            print(self.terminal.move_xy(ox, oy + i) + msg)

    def get_layout_graph(self, game):
        bw, bh = game.board_size
        sh = self.STATE_HEIGHT
        ox, oy = self.get_board_origin_coords(game)

        vertices = [
            Vertex(ox - 1, oy - 1), 
            Vertex(ox + bw, oy - 1),
            Vertex(ox + bw, oy + bh),
            Vertex(ox + bw, oy + bh + sh),
            Vertex(ox - 1, oy + bh + sh),
            Vertex(ox - 1, oy + bh)
        ]
        edges = [
            Edge(vertices[0], vertices[1]),
            Edge(vertices[1], vertices[2]),
            Edge(vertices[2], vertices[3]),
            Edge(vertices[3], vertices[4]),
            Edge(vertices[4], vertices[5]),
            Edge(vertices[5], vertices[0]),
            Edge(vertices[5], vertices[2]),
        ]
        graph = Graph(vertices, edges)
        if game.debug:
            dw = self.DEBUG_WIDTH
            graph.vertices.append(Vertex(ox + bw + dw, oy - 1))
            graph.vertices.append(Vertex(ox + bw + dw, oy + bh + sh))
            graph.edges.append(Edge(graph.vertices[1], graph.vertices[6]))
            graph.edges.append(Edge(graph.vertices[6], graph.vertices[7]))
            graph.edges.append(Edge(graph.vertices[3], graph.vertices[7]))
        return graph

    def terminal_size_changed(self):
        return self.terminal_size != (self.terminal.width, self.terminal.height)

    def check_terminal_size(self, game):
        bw, bh = game.board_size
        width_needed = bw + self.BORDER_X
        height_needed = bh + self.BORDER_Y + self.STATE_HEIGHT
        if self.terminal.width < width_needed:
            raise TerminalTooSmall(width=self.terminal.width, width_needed=width_needed)
        elif self.terminal.height < height_needed:
            raise TerminalTooSmall(height=self.terminal.height, height_needed=height_needed)

    def board_origin(self, game):
        x, y = self.get_board_origin_coords(game)
        return self.terminal.move_xy(x, y)

    def get_board_origin_coords(self, game):
        bw, bh = game.board_size
        margin_top = (self.terminal.height - bh - self.BORDER_Y) // 2
        if game.debug:
            margin_left = (self.terminal.width - bw - self.DEBUG_WIDTH - self.BORDER_X) // 2
        else:
            margin_left = (self.terminal.width - bw - self.BORDER_X) // 2
        return margin_left, margin_top

    def get_state_origin_coords(self, game):
        bw, bh = game.board_size
        ox, oy = self.get_board_origin_coords(game)
        return ox, oy + bh + 1

    def get_debug_origin_coords(self, game):
        bw, bh = game.board_size
        ox, oy = self.get_board_origin_coords(game)
        return ox + bw + 1, oy


