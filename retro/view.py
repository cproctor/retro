from retro.graph import Vertex, Edge, Graph
from retro.errors import TerminalTooSmall

class View:
    BORDER_X = 2
    BORDER_Y = 3
    STATE_HEIGHT = 5
    DEBUG_WIDTH = 60

    def __init__(self, terminal, board_size, debug=False):
        self.terminal = terminal
        self.board_size = board_size
        self.debug = debug

    def render(self, game):
        self.render_layout()
        ox, oy = self.get_board_origin_coords()
        for agent in sorted(game.agents, key=lambda a: getattr(a, 'z', 0)):
            ax, ay = agent.position
            print(self.terminal.move_xy(ox + ax, oy + ay) + agent.character)

    def render_layout(self):
        bw, bh = self.board_size
        self.check_terminal_size()
        print(self.terminal.clear)
        layout_graph = self.get_layout_graph()
        layout_graph.render(self.terminal)

    def get_layout_graph(self):
        bw, bh = self.board_size
        sh = self.STATE_HEIGHT
        ox, oy = self.get_board_origin_coords()

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
        if self.debug:
            dw = self.DEBUG_WIDTH
            graph.vertices.append(Vertex(ox + bw + dw, oy - 1))
            graph.vertices.append(Vertex(ox + bw + dw, oy + bh + sh))
            graph.edges.append(Edge(graph.vertices[1], graph.vertices[6]))
            graph.edges.append(Edge(graph.vertices[6], graph.vertices[7]))
            graph.edges.append(Edge(graph.vertices[3], graph.vertices[7]))
        return graph

    def check_terminal_size(self):
        bw, bh = self.board_size
        width_needed = bw + self.BORDER_X
        height_needed = bh + self.BORDER_Y + self.STATE_HEIGHT
        if self.terminal.width < width_needed:
            raise TerminalTooSmall(width=self.terminal.width, width_needed=width_needed)
        elif self.terminal.height < height_needed:
            raise TerminalTooSmall(height=self.terminal.height, height_needed=height_needed)

    def board_origin(self):
        x, y = self.get_board_origin_coords()
        return self.terminal.move_xy(x, y)

    def get_board_origin_coords(self):
        bw, bh = self.board_size
        margin_top = (self.terminal.height - bh - self.BORDER_Y) // 2
        if self.debug:
            margin_left = (self.terminal.width - bw - self.DEBUG_WIDTH - self.BORDER_X) // 2
        else:
            margin_left = (self.terminal.width - bw - self.BORDER_X) // 2
        return margin_left, margin_top


