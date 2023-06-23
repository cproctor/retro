class Graph:

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def __str__(self):
        return '\n'.join(str(e) for e in self.edges)

    def draw(self, terminal):
        for v in self.vertices:
            v.draw(terminal)
        for e in self.edges:
            e.draw(terminal)

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

    def neighbors(self):
        vertices = []
        for edge in self.edges:
            if self == edge.begin:
                vertices.append(edge.end)
            else:
                vertices.append(edge.begin)
        return vertices

    def draw(self, terminal):
        print(terminal.move_xy(self.x, self.y) + self.get_character())

    def get_character(self):
        u = self.has_up_edge()
        r = self.has_right_edge()
        d = self.has_down_edge()
        l = self.has_left_edge()
        code = ''.join([str(int(direction)) for direction in [u, r, d, l]])
        return self.CHARACTERS[code]

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

    def draw(self, terminal):
        if self.is_horizontal():
            with terminal.location(self.begin.x + 1, self.begin.y):
                line = "═" * (self.end.x - self.begin.x - 1)
                print(line)
        else:
            for y in range(self.begin.y + 1, self.end.y):
                print(terminal.move_xy(self.begin.x, y) + "║")

    def is_horizontal(self):
        return self.begin.y == self.end.y

    def is_vertical(self):
        return self.begin.x == self.end.x
