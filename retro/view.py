from retro.errors import TerminalTooSmall

class View:
    BORDER_X = 2
    BORDER_Y = 3
    STATE_HEIGHT = 5
    DEBUG_WIDTH = 20

    def __init__(self, terminal, board_size, debug=False):
        self.terminal = terminal
        self.board_size = board_size

    def render(self):
        pass


    def render_layout(self):
        bw, bh = self.board_size
        self.check_terminal_size()
        self.terminal.clear()
        print(self.board_origin() + '╔' + ('═' * bw) + '╗')

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
        margin_left = (self.terminal.width - bw - self.BORDER_X) // 2
        margin_top = (self.terminal.height - bh - self.BORDER_Y) // 2
        return margin_left, margin_top


