from retro.graph import Vertex, Edge, Graph
from retro.views._util import get_agent_character
from retro.errors import TerminalTooSmall

identity = lambda x: x


def vector_add(vec0, vec1):
    x0, y0 = vec0
    x1, y1 = vec1
    return (x0 + x1, y0 + y1)


class TerminalView:
    BORDER_X = 2
    BORDER_Y = 3
    DEBUG_WIDTH = 60

    def __init__(self, terminal, color='white_on_black'):
        self.terminal = terminal
        self.terminal_size = (self.terminal.width, self.terminal.height)
        self.color = color
        self.initial_render = True

    def on_game_start(self, game) -> None:
        pass

    def render(self, game) -> None:
        if self.initial_render or self.terminal_size_changed():
            self.terminal_size = (self.terminal.width, self.terminal.height)
            self.render_layout(game)
        if self.initial_render or game.state.changed:
            self.render_state(game)
        if game.debug:
            self.render_debug_log(game)
        prior_board_view = self.get_board_view(
            game.prior_agent_positions,
            game.prior_view_position,
            game.view_size
        )
        board_view = self.get_board_view(
            game.agent_positions,
            game.view_position,
            game.view_size
        )
        diff = self.get_board_view_diff(prior_board_view, board_view)
        self.render_board_view(diff, game)
        self.initial_render = False

    def get_board_view(self, agent_positions, view_position, view_size):
        vox, voy = view_position
        vx, vy = view_size
        board_view = {}
        for position, agents in agent_positions.items():
            x, y = position
            if vox <= x < vox + vx and voy <= y < voy + vy:
                top = max(agents, key=lambda a: getattr(a, 'z', 0) or 0)
                color = self.get_color(top.color) if hasattr(top, 'color') else identity
                board_view[(x - vox, y - voy)] = color(get_agent_character(top, (x, y)))
        return board_view

    def get_board_view_diff(self, board_view_0, board_view_1):
        diff = {}
        positions = set(board_view_0.keys()).union(board_view_1.keys())
        for p in positions:
            if p not in board_view_0:
                diff[p] = board_view_1[p]
            elif p not in board_view_1:
                diff[p] = self.get_color(self.color)(' ')
            elif board_view_0[p] != board_view_1[p]:
                diff[p] = board_view_1[p]
        return diff

    def render_board_view(self, board_view, game):
        origin = self.get_view_origin_coords(game)
        for position, colored_character in board_view.items():
            x, y = vector_add(origin, position)
            print(self.terminal.move_xy(x, y) + colored_character)

    def render_layout(self, game):
        self.check_terminal_size(game)
        self.clear_screen()
        layout_graph = self.get_layout_graph(game)
        layout_graph.render(self.terminal)

    def clear_screen(self):
        print(self.terminal.home + self.get_color(self.color) + self.terminal.clear)

    def get_color(self, color_string):
        if not hasattr(self.terminal, color_string):
            msg = (
                f"{color_string} is not a supported color. "
                "See https://blessed.readthedocs.io/en/latest/colors.html"
            )
            raise ValueError(msg)
        return getattr(self.terminal, color_string)

    def render_state(self, game):
        vw, vh = game.view_size
        ox, oy = self.get_state_origin_coords(game)
        color = self.get_color(self.color)
        for i, key in enumerate(sorted(game.state.keys())):
            msg = f"{key}: {game.state[key]}"[:vw].ljust(vw)
            print(self.terminal.move_xy(ox, oy + i) + color(msg))

    def render_debug_log(self, game):
        vw, vh = game.view_size
        debug_height = vh + self.state_height(game)
        ox, oy = self.get_debug_origin_coords(game)
        color = self.get_color(self.color)
        for i, (turn_number, message) in enumerate(game.log_messages[-debug_height:]):
            msg = f"{turn_number}. {message}"[:self.DEBUG_WIDTH - 1].ljust(self.DEBUG_WIDTH - 1)
            print(self.terminal.move_xy(ox, oy + i) + color(msg))

    def get_layout_graph(self, game):
        vw, vh = game.view_size
        sh = self.state_height(game)
        ox, oy = self.get_view_origin_coords(game)
        vertices = [
            Vertex(ox - 1, oy - 1),
            Vertex(ox + vw, oy - 1),
            Vertex(ox + vw, oy + vh),
            Vertex(ox + vw, oy + vh + sh),
            Vertex(ox - 1, oy + vh + sh),
            Vertex(ox - 1, oy + vh)
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
            graph.vertices.append(Vertex(ox + vw + dw, oy - 1))
            graph.vertices.append(Vertex(ox + vw + dw, oy + vh + sh))
            graph.edges.append(Edge(graph.vertices[1], graph.vertices[6]))
            graph.edges.append(Edge(graph.vertices[6], graph.vertices[7]))
            graph.edges.append(Edge(graph.vertices[3], graph.vertices[7]))
        return graph

    def terminal_size_changed(self):
        return self.terminal_size != (self.terminal.width, self.terminal.height)

    def check_terminal_size(self, game):
        vw, vh = game.view_size
        width_needed = vw + self.BORDER_X
        height_needed = vh + self.BORDER_Y + self.state_height(game)
        if self.terminal.width < width_needed:
            raise TerminalTooSmall(width=self.terminal.width, width_needed=width_needed)
        elif self.terminal.height < height_needed:
            raise TerminalTooSmall(height=self.terminal.height, height_needed=height_needed)

    def view_origin(self, game):
        x, y = self.get_view_origin_coords(game)
        return self.terminal.move_xy(x, y)

    def get_view_origin_coords(self, game):
        vw, vh = game.view_size
        margin_top = (self.terminal.height - vh - self.BORDER_Y) // 2
        if game.debug:
            margin_left = (self.terminal.width - vw - self.DEBUG_WIDTH - self.BORDER_X) // 2
        else:
            margin_left = (self.terminal.width - vw - self.BORDER_X) // 2
        return margin_left, margin_top

    def state_height(self, game):
        return max(len(game.state), 1)

    def get_state_origin_coords(self, game):
        vw, vh = game.view_size
        ox, oy = self.get_view_origin_coords(game)
        return ox, oy + vh + 1

    def get_debug_origin_coords(self, game):
        vw, vh = game.view_size
        ox, oy = self.get_view_origin_coords(game)
        return ox + vw + 1, oy
