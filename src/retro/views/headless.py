from retro.views._util import get_agent_character


class HeadlessView:
    """Maintains a readable board state without any terminal output.
    After each game.step(), board_characters reflects the current board.
    board_characters[y][x] is the character at position (x, y), or ' ' if empty.
    """

    def __init__(self):
        self.board_characters: list[list[str]] = []

    def on_game_start(self, game) -> None:
        bw, bh = game.board_size
        self.board_characters = [[' '] * bw for _ in range(bh)]

    def render(self, game) -> None:
        bw, bh = game.board_size
        board = [[' '] * bw for _ in range(bh)]
        for (x, y), agents in game.get_agents_by_position().items():
            top = max(agents, key=lambda a: getattr(a, 'z', 0) or 0)
            board[y][x] = get_agent_character(top, (x, y))
        self.board_characters = board
