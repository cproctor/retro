import json
from collections import defaultdict
from signal import signal, SIGWINCH
from time import sleep, perf_counter
from blessed import Terminal
from retro.views.terminal import TerminalView
from retro.input import TerminalInput
from retro.change_dict import ChangeDict
from retro.agent import Tombstone
from retro.validation import (
    validate_agent,
    validate_state,
    validate_agent_name,
    validate_position,
)
from retro.errors import (
    AgentWithNameAlreadyExists,
    AgentNotFoundByName,
    AgentAlreadyInGame,
    IllegalMove,
)


def agent_occupied_positions(agent):
    """Returns all board positions occupied by an agent."""
    x, y = agent.position
    size = getattr(agent, 'size', None)
    if size is None:
        return [(x, y)]
    w, h = size
    return [(x + dx, y + dy) for dy in range(h) for dx in range(w)]


class Game:
    """
    Creates a playable game.

    Arguments:
        agents (list): A list of agents to add to the game.
        state (dict): A dict containing the game's initial state.
        board_size (int, int): (Optional, default ``(64, 32)``) The two-dimensional size
            of the game board.
        view_size (int, int): (Optional, default is ``board_size``) The two-dimensional size
            of the view.
        view_position (int, int): (Optional) The (x, y) coordinates of the top left corner
            of the view. By default, this is (0, 0).
        debug (bool): (Optional) Turn on debug mode, showing log messages while playing.
        framerate (int): (Optional) The target number of frames per second at which the
            game should run.
        color (str): (Optional) The game's background color scheme.
        wait_for_enter (bool): (Optional) If True, the game screen stays open after the
            game ends until Enter or Escape is pressed. Defaults to False.
        show_state (bool): (Optional) If False, ``TerminalView`` does not display the
            state dict below the board. Defaults to True. Useful for games with small
            boards or many state keys, where the state pane would otherwise be
            unreadably narrow or require an oversized terminal.
        dump_state (str): (Optional) A filename. If provided, the game state will be saved
            to that file as JSON when the game ends.
        log_file (str): (Optional) A filename. If provided, all log messages are written
            to this file in real time.
        input_source: (Optional) An :class:`retro.input.InputSource` instance. When
            provided, ``step()`` uses it for input instead of the terminal. Ignored by
            ``play()``, which always uses terminal input.
        view: (Optional) A view instance (implements ``on_game_start`` and ``render``).
            When provided, ``step()`` calls ``view.render(self)`` after each turn.
            Ignored by ``play()``, which manages its own :class:`retro.views.TerminalView`.

    ::

        # Standard interactive play:
        from retro.game import Game
        from retro.agent import ArrowKeyAgent
        game = Game([ArrowKeyAgent()], {})
        game.play()

        # Programmatic stepping (e.g. for training):
        from retro.input import ProgrammaticInput
        from retro.views import HeadlessView
        inp = ProgrammaticInput()
        view = HeadlessView()
        game = Game([MyAgent()], {'score': 0}, input_source=inp, view=view)
        game.start()
        inp.press('KEY_RIGHT')
        game.step()
        board = view.board_characters
    """

    STATE_HEIGHT = 5
    EXIT_CHARACTERS = ("KEY_ENTER", "KEY_ESCAPE")

    @property
    def view_position(self):
        return self._view_position

    @view_position.setter
    def view_position(self, position):
        if position != self.view_position:
            self._view_position = position
            self.view_position_changed = True

    def __init__(self, agents, state, board_size=(64, 32), view_size=None,
                 view_position=(0, 0), debug=False, framerate=24, color="white_on_black",
                 wait_for_enter=False, dump_state=None, log_file=None,
                 input_source=None, view=None, show_state=True):
        self.log_messages = []
        self.agents_by_name = {}
        self.agents = []
        validate_state(state)
        self.state = ChangeDict(state)
        self.board_size = board_size
        self.view_size = view_size or board_size
        self._view_position = view_position
        self.view_position_changed = True
        self.debug = debug
        self.framerate = framerate
        self.turn_number = 0
        self.color = color
        self.wait_for_enter = wait_for_enter
        self.show_state = show_state
        self.dump_state = dump_state
        self.log_file = log_file
        self.input_source = input_source
        self.view = view
        self.playing = False
        self.agent_positions = {}
        self.prior_agent_positions = {}
        self.prior_view_position = view_position
        if log_file:
            open(log_file, 'w').close()
        self._position_cache = None
        for agent in agents:
            self.add_agent(agent)

    def start(self):
        """Initialize game state before the first ``step()`` call.
        Call this when using ``step()`` directly (without ``play()``).
        """
        self.playing = True
        self.state.changed = True
        if self.view is not None:
            self.view.on_game_start(self)

    def step(self):
        """Run one game turn: collect input, let each agent act, advance state.

        Call ``start()`` before the first ``step()``.
        After ``step()`` returns, ``self.playing`` reflects whether the game is still active.
        If a :class:`retro.views.View` was provided at construction, its ``render()`` is
        called at the end of each step.
        """
        self.turn_number += 1
        self.keys_pressed = self.input_source.collect()
        if self.debug and self.keys_pressed:
            self.log("Keys: " + ', '.join(k.name or str(k) for k in self.keys_pressed))
        self.prior_view_position = self.view_position
        self.prior_agent_positions = self.agent_positions
        for agent in self.agents:
            if hasattr(agent, 'handle_keystroke'):
                for key in self.keys_pressed:
                    agent.handle_keystroke(key, self)
            if hasattr(agent, 'play_turn'):
                agent.play_turn(self)
                self._position_cache = None
            if getattr(agent, 'display', True):
                for pos in agent_occupied_positions(agent):
                    if not self.on_board(pos):
                        raise IllegalMove(agent, pos)
        self.agent_positions = self.get_agents_by_position()
        if self.view is not None:
            self.view.render(self)
        self.state.changed = False
        self.view_position_changed = False

    def play(self, input_source=None):
        """Start the game in a terminal with interactive input and rendering.

        Arguments:
            input_source: (Optional) An :class:`retro.input.InputSource` to use
                instead of the keyboard. When omitted, arrow-key / character
                input is read from the terminal as normal.
        """
        self.playing = True
        terminal = Terminal()
        self.input_source = input_source or TerminalInput(terminal)
        with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
            term_view = TerminalView(terminal, color=self.color, show_state=self.show_state)
            _saved_view = self.view
            self.view = term_view
            self.agent_positions = {}
            self.prior_agent_positions = {}
            self.state.changed = True
            term_view.on_game_start(self)
            while self.playing:
                turn_start_time = perf_counter()
                self.step()
                turn_end_time = perf_counter()
                time_elapsed_in_turn = turn_end_time - turn_start_time
                time_remaining_in_turn = max(0, 1 / self.framerate - time_elapsed_in_turn)
                sleep(time_remaining_in_turn)
            self.view = _saved_view
            if self.dump_state:
                with open(self.dump_state, 'w') as f:
                    json.dump(dict(self.state), f)
            if self.wait_for_enter:
                while True:
                    if terminal.inkey().name in self.EXIT_CHARACTERS:
                        break

    def log(self, message):
        """Write a log message.

        Arguments:
            message (str): The message to log.
        """
        self.log_messages.append((self.turn_number, message))
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(f"{self.turn_number}: {message}\n")

    def end(self):
        """End the game. No more turns will run."""
        self.playing = False

    def add_agent(self, agent):
        """Add an agent to the game.

        Arguments:
            agent: An instance of an agent class.
        """
        validate_agent(agent)
        if agent in self.agents:
            raise AgentAlreadyInGame(agent)
        if getattr(agent, "display", True):
            for pos in agent_occupied_positions(agent):
                if not self.on_board(pos):
                    raise IllegalMove(agent, pos)
        if hasattr(agent, "name"):
            if agent.name in self.agents_by_name:
                raise AgentWithNameAlreadyExists(agent.name)
            self.agents_by_name[agent.name] = agent
        self.agents.append(agent)

    def get_agent_by_name(self, name):
        """Look up an agent by name.

        Arguments:
            name (str): The agent's name.

        Returns:
            An agent.
        """
        validate_agent_name(name)
        if name in self.agents_by_name:
            return self.agents_by_name[name]
        else:
            raise AgentNotFoundByName(name)

    def is_empty(self, position):
        """Check whether a position is unoccupied.

        Arguments:
            position (int, int): The position to check.

        Returns:
            A bool
        """
        return position not in self.get_agents_by_position()

    def get_agents_by_position(self):
        """Return a dict mapping each occupied position to a list of agents there."""
        if self._position_cache is not None:
            return self._position_cache
        positions = defaultdict(list)
        for agent in self.agents:
            if getattr(agent, "display", True):
                for pos in agent_occupied_positions(agent):
                    positions[pos].append(agent)
        self._position_cache = positions
        return positions

    def on_view(self, position):
        """Check whether a position is within the current view.

        Arguments:
            position (int, int): The position to check.

        Returns:
            A bool
        """
        validate_position(position)
        x, y = position
        vox, voy = self.view_position
        vw, vh = self.view_size
        return vox <= x < vox + vw and voy <= y < voy + vh

    def remove_agent(self, agent):
        """Remove an agent from the game.

        Arguments:
            agent (Agent): the agent to remove.
        """
        if agent not in self.agents:
            raise AgentNotInGame(agent)
        else:
            self.agents.remove(agent)
            if hasattr(agent, "name"):
                self.agents_by_name.pop(agent.name)

    def remove_agent_by_name(self, name):
        """Remove an agent from the game by name.

        Arguments:
            name (str): the agent's name.
        """
        validate_agent_name(name)
        if name not in self.agents_by_name:
            raise AgentNotFoundByName(name)
        agent = self.agents_by_name.pop(name)
        self.agents.remove(agent)

    def on_board(self, position):
        """Check whether a position is on the game board.

        Arguments:
            position (int, int): The position to check.

        Returns:
            A bool
        """
        x, y = position
        bx, by = self.board_size
        return x >= 0 and x < bx and y >= 0 and y < by
