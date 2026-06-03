class Agent:
    """Represents a character in the game. To create an Agent, define a new
    class with some of the attributes and methods below. You may change any of
    the Agent's attributes at any time, and the result will immediately be 
    visible in the game.

    After you create your Agents, add them to the ``Game``, either when it is created
    or using ``Game.add_agent`` later on. Then the Game will take care of calling 
    the Agent's methods at the appropriate times. 

    Attributes:
        position: (Required) The agent's ``(int, int)`` position on the board.
            For single-cell agents this is the agent's location. For multi-cell
            agents (when ``size`` is set) this is the top-left corner of the
            agent's bounding box. The agent is only displayed when every cell it
            occupies is on the board; an :py:exc:`retro.errors.IllegalMove` is
            raised if any cell falls off the board.
        character: (Required unless ``display`` is ``False``.) The visual
            representation of the agent. For single-cell agents, a one-character
            string displayed at ``position``. When ``size`` is set, this may
            instead be a list of strings — one per row from top to bottom — where
            each string supplies the characters for that row from left to right.
            Any cell whose row or column index falls outside the provided strings
            is rendered as a blank space.
        name: (Optional) If an agent has a name, it must be unique within the game.
            Agent names can be used to look up agents with
            :py:meth:`retro.game.Game.get_agent_by_name`.
        color (str): (Optional) The agent's color.
            `Available colors <https://blessed.readthedocs.io/en/latest/colors.html>`_.
        display: (Optional) When ``False``, the Agent will not be displayed on the
            board. This is useful when you want to create an agent which will be displayed
            later, or when you want to create an agent which acts on the Game indirectly,
            for example by spawning other Agents. Defaults to True.
        z: (Optional) When multiple Agents overlap at the same cell, the agent with
            the highest ``z`` value is displayed at that cell. The Game is played on a
            two-dimensional (x, y) board, but you can think of ``z`` as a third "up"
            dimension. Defaults to 0.
        size: (Optional) A ``(width, height)`` tuple declaring how many board cells
            this agent occupies. ``position`` is the top-left corner; the agent spans
            ``width`` columns and ``height`` rows from there. When ``size`` is set,
            ``character`` may be a list of strings (one per row) to give each cell a
            distinct character. When omitted, the agent occupies a single cell.
    """
    character = "*"
    position = (0, 0)
    name = "agent"
    color = "white_on_black"
    display = True
    z = 0

    def play_turn(self, game):
        """If an Agent has this method, it will be called once 
        each turn. 

        Arguments: 
            game (Game): The game which is currently being played will be 
                passed to the Agent, in case it needs to check anything about
                the game or make any changes. 
        """
        pass

    def handle_keystroke(self, keystroke, game):
        """If an Agent has a this method, it will be called every
        time a key is pressed in the game.

        Arguments: 
            keystroke (blessed.keyboard.Keystroke): The key which was pressed. You can 
                compare a Keystroke with a string (e.g. ``if keystroke == 'q'``) to check 
                whether it is a regular letter, number, or symbol on the keyboard. You can 
                check special keys using the keystroke's name 
                (e.g. ``if keystroke.name == "KEY_RIGHT"``). Run your game in debug mode to 
                see the names of keystrokes. 
            game (Game): The game which is currently being played will be 
                passed to the Agent, in case it needs to check anything about
                the game or make any changes. 
            
        """
        pass

class ArrowKeyAgent:
    """A simple agent which can be moved around with the arrow keys.
    """
    name = "ArrowKeyAgent"
    character = "*"
    position = (0,0)
    display = True
    z = 0

    def play_turn(self, game):
        if hasattr(super(), 'play_turn'):
            super().play_turn(game)

    def handle_keystroke(self, keystroke, game):
        """Moves the agent's position if the keystroke is one of the arrow keys.
        One by one, checks the keystroke's name against each arrow key. 
        Then uses :py:meth:`try_to_move` to check whether the move is on the 
        game's board before moving.
        """
        x, y = self.position
        if keystroke.name == "KEY_RIGHT":
            self.try_to_move((x + 1, y), game)
        elif keystroke.name == "KEY_UP":
            self.try_to_move((x, y - 1), game)
        elif keystroke.name == "KEY_LEFT":
            self.try_to_move((x - 1, y), game)
        elif keystroke.name == "KEY_DOWN":
            self.try_to_move((x, y + 1), game)

    def try_to_move(self, position, game):
        """Moves to the position if it is on the game board. 
        """
        if game.on_board(position):
            self.position = position
            game.log(f"Position: {self.position}")

class CenterViewAgent:
    """An agent which centers the game view on the agent.
    If margin is an integer, then the view will only re-center
    when the agent is within ``margin`` spaces of the edge of the view.
    If margin is None (default), the view re-centers every turn.

    Attributes:
        margin (int or None): Distance from the viewport edge that triggers
            re-centering. Defaults to None (always re-center).
    """
    margin = None

    def play_turn(self, game):
        if hasattr(super(), 'play_turn'):
            super().play_turn(game)
        if self.needs_to_center_view(game):
            self.center_view(game)

    def center_view(self, game):
        """Centers the game view on this agent.

        Arguments:
            game (Game): The current game.
        """
        vw, vh = game.view_size
        bw, bh = game.board_size
        x, y = self.position
        new_x = max(0, min(x - vw // 2, bw - vw))
        new_y = max(0, min(y - vh // 2, bh - vh))
        game.view_position = (new_x, new_y)

    def needs_to_center_view(self, game):
        """Returns True if the view should be re-centered this turn.

        Arguments:
            game (Game): The current game.
        """
        if self.margin is None:
            return True
        return self.distance_to_edge_of_view(game) <= self.margin

    def distance_to_edge_of_view(self, game):
        """Returns the shortest distance from this agent to any edge of the
        current view.

        Arguments:
            game (Game): The current game.
        """
        x, y = self.position
        vox, voy = game.view_position
        vw, vh = game.view_size
        return min(x - vox, vox + vw - 1 - x, y - voy, voy + vh - 1 - y)


class Tombstone:
    """A placeholder for a missing agent.
    """
    def __init__(self, position, color):
        self.position = position
        self.color = color

    character = ' '
