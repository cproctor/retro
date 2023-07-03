from retro.graph import Vertex, Edge, Graph
from retro.errors import TerminalTooSmall

class View:
    BORDER_X = 2
    BORDER_Y = 3
    STATE_HEIGHT = 5
    DEBUG_WIDTH = 60

    def __init__(self, terminal):
        self.terminal = terminal

    def render(self, game):
        self.render_layout(game)
        ox, oy = self.get_board_origin_coords(game)
        self.render_state(game)
        if game.debug:
            self.render_debug_log(game)
        for agent in sorted(game.agents, key=lambda a: getattr(a, 'z', 0)):
            if getattr(agent, 'display', True):
                ax, ay = agent.position
                print(self.terminal.move_xy(ox + ax, oy + ay) + agent.character)

    def render_layout(self, game):
        bw, bh = game.board_size
        self.check_terminal_size(game)
        print(self.terminal.clear)
        layout_graph = self.get_layout_graph(game)
        layout_graph.render(self.terminal)

    def render_state(self, game):
        bw, bh = game.board_size
        ox, oy = self.get_state_origin_coords(game)
        for i, key in enumerate(sorted(game.state.keys())):
            msg = f"{key}: {game.state[key]}"[:bw]
            print(self.terminal.move_xy(ox, oy + i) + msg)

    def render_debug_log(self, game):
        bw, bh = game.board_size
        debug_height = bh + self.STATE_HEIGHT 
        ox, oy = self.get_debug_origin_coords(game)
        for i, (turn_number, message) in enumerate(game.log_messages[-debug_height:]):
            msg = f"{turn_number}. {message}"[:self.DEBUG_WIDTH]
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


