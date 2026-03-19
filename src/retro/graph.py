from retro.errors import GraphError

class Graph:
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices or []
        self.edges = edges or []

    def __str__(self):
        return '\n'.join(str(e) for e in self.edges)

    def get_or_create_vertex(self, x, y):
        for v in self.vertices:
            if x == v.x and y == v.y:
                return v
        for e in self.edges:
            if e.crosses(x, y):
                return self.split_edge(e, x, y)
        new_vertex = Vertex(x, y)
        self.vertices.append(new_vertex)
        return new_vertex

    def get_or_create_edge(self, x0, y0, x1, y1):
        v0 = self.get_or_create_vertex(x0, y0)
        v1 = self.get_or_create_vertex(x1, y1)
        new_edge = Edge(v0, v1)
        for e in self.edges:
            if e == new_edge:
                new_edge.remove()
                return e
        self.edges.append(new_edge)
        return new_edge

    def split_edge(self, edge, x, y):
        """
        Splits an edge by inserting a new vertex along the edge. 
        """
        if not edge.crosses(x, y):
            raise GraphError(f"Can't split edge {edge} at ({x}, {y})")
        self.remove_edge(edge)
        v = Vertex(x, y)
        self.vertices.append(v)
        self.edges.append(Edge(edge.begin, v))
        self.edges.append(Edge(v, edge.end))
        return v

    def remove_edge(self, edge):
        if edge not in self.edges:
            raise GraphError(f"Edge {edge} is not in the graph")
        self.edges.remove(edge)
        edge.begin.edges.remove(edge)
        edge.end.edges.remove(edge)

    def render(self, terminal):
        for v in self.vertices:
            v.render(terminal)
        for e in self.edges:
            e.render(terminal)

    def get_layout(self):
        """Returns a list of (x, y, character)
        """
        layout = []
        for edge in self.edges:
            layout += edge.get_layout()
        for vertex in self.vertices:
            layout += vertex.get_layout()
        return layout

    def get_agents(self):
        "Return agents corresponding to this Graph, for use in-game."
        agents = [v.get_agent() for v in self.vertices]
        for e in self.edges:
            agents += e.get_agents()
        return agents

class Vertex:
    CHARACTERS = {
        "0000": " ",
        "0001": "═",
        "0010": "║",
        "0011": "╗",
        "0100": "═",
        "0101": "═",
        "0110": "╔",
        "0111": "╦",
        "1000": "║",
        "1001": "╝",
        "1010": "║",
        "1011": "╣",
        "1100": "╚",
        "1101": "╩",
        "1110": "╠",
        "1111": "╬",
    }
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def neighbors(self):
        vertices = []
        for edge in self.edges:
            if self == edge.begin:
                vertices.append(edge.end)
            else:
                vertices.append(edge.begin)
        return vertices

    def render(self, terminal):
        print(terminal.move_xy(self.x, self.y) + self.get_character())

    def get_agent(self):
        return GraphAgent(self.get_character(), (self.x, self.y))

    def get_character(self):
        u = self.has_up_edge()
        r = self.has_right_edge()
        d = self.has_down_edge()
        l = self.has_left_edge()
        code = ''.join([str(int(direction)) for direction in [u, r, d, l]])
        return self.CHARACTERS[code]

    def get_layout(self):
        return [(self.x, self.y, self.get_character())]

    def has_up_edge(self):
        return any([v.x == self.x and v.y < self.y for v in self.neighbors()])

    def has_right_edge(self):
        return any([v.y == self.y and self.x < v.x for v in self.neighbors()])

    def has_down_edge(self):
        return any([v.x == self.x and self.y < v.y for v in self.neighbors()])

    def has_left_edge(self):
        return any([v.y == self.y and v.x < self.x for v in self.neighbors()])

class Edge:
    def __init__(self, begin, end):
        if not isinstance(begin, Vertex) or not isinstance(end, Vertex):
            raise ValueError("Tried to initialize an Edge with a non-vertex")
        if begin.x < end.x or begin.y < end.y:
            self.begin = begin
            self.end = end
        else:
            self.begin = end
            self.end = begin
        if not (self.is_horizontal() or self.is_vertical()):
            raise ValueError("Edges must be horizontal or vertical.")
        if self.is_horizontal() and self.is_vertical():
            raise ValueError("Self-edges are not allowed.")
        self.begin.edges.append(self)
        self.end.edges.append(self)

    def __str__(self):
        return f"{self.begin} -> {self.end}"

    def render(self, terminal):
        if self.is_horizontal():
            with terminal.location(self.begin.x + 1, self.begin.y):
                line = "═" * (self.end.x - self.begin.x - 1)
                print(line)
        else:
            for y in range(self.begin.y + 1, self.end.y):
                print(terminal.move_xy(self.begin.x, y) + "║")

    def get_layout(self):
        if self.is_horizontal():
            return [(x, self.begin.y, "=") for x in range(self.begin.x, self.end.x)]
        else:
            return [(self.begin.x, y, "║") for y in range(self.begin.y, self.end.y)]

    def get_agents(self):
        if self.is_horizontal():
            return [GraphAgent("=", (i, self.begin.y)) for i in range(self.begin.x + 1, self.end.x)]
        else:
            return [GraphAgent("║", (self.begin.x, j)) for j in range(self.begin.y + 1, self.end.y)]

    def is_horizontal(self):
        return self.begin.y == self.end.y

    def is_vertical(self):
        return self.begin.x == self.end.x

    def crosses(self, x, y):
        if self.is_horizontal():
            return self.begin.y == y and self.begin.x < x and x < self.end.x
        else:
            return self.begin.x == x and self.begin.y < y and y < self.end.y

    def remove(self):
        self.begin.edges.remove(self)
        self.end.edges.remove(self)

class GraphAgent:
    """An agent class for graph characters.
    """
    def __init__(self, character, position):
        self.character = character
        self.position = position

    def __repr__(self):
        return f"<GraphAgent {self.character} {self.position}>"
