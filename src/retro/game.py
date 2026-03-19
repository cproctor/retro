import json
from collections import defaultdict
from signal import signal, SIGWINCH
from time import sleep, perf_counter
from blessed import Terminal
from retro.view import View
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
    You will use Game to create games, but don't need to read or understand how
    this class works. The main work in creating a 

    Arguments: 
        agents (list): A list of agents to add to the game. 
        state (dict): A dict containing the game's initial state. 
        board_size (int, int): (Optional, default `(64, 32)`) The two-dimensional size 
            of the game board.
        view_size (int, int): (Optional, default is `board_size`) The two-dimensional size
            of the view. 
        view_position (int, int): (Optional) The (x, y) coordinates of the top left corner
            of the view. By default, this is (0, 0).
        debug (bool): (Optional) Turn on debug mode, showing log messages while playing.
        framerate (int): (Optional) The target number of frames per second at which the 
            game should run.
        color (str): (Optional) The game's background color scheme. `Available colors <https://blessed.readthedocs.io/en/latest/colors.html>`_.
        wait_for_enter (bool): (Optional) If True, the game screen stays open after the game ends until Enter or Escape is pressed. Defaults to False.
        dump_state (str): (Optional) A filename. If provided, the game state will be saved to that file as JSON when the game ends.

    ::

        # This example will create a simple game.
        from retro.game import Game
        from retro.agent import ArrowKeyAgent

        agents = [ArrowKeyAgent()]
        state = {}
        game = Game(agents, state)
        game.play()
        
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
            wait_for_enter=False, dump_state=None):
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
        self.dump_state = dump_state
        self._position_cache = None
        for agent in agents:
            self.add_agent(agent)

    def play(self):
        """Starts the game.
        """
        self.playing = True
        terminal = Terminal()
        with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
            view = View(terminal, color=self.color)
            self.agent_positions = {}
            self.state.changed = True
            while self.playing:
                turn_start_time = perf_counter()
                self.turn_number += 1
                self.keys_pressed = self.collect_keystrokes(terminal)
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
                view.render(self)
                self.state.changed = False
                self.view_position_changed = False
                turn_end_time = perf_counter()
                time_elapsed_in_turn = turn_end_time - turn_start_time
                time_remaining_in_turn = max(0, 1/self.framerate - time_elapsed_in_turn)
                sleep(time_remaining_in_turn)
            if self.dump_state:
                with open(self.dump_state, 'w') as f:
                    json.dump(dict(self.state), f)
            if self.wait_for_enter:
                while True:
                    if terminal.inkey().name in self.EXIT_CHARACTERS:
                        break

    def collect_keystrokes(self, terminal):
        keys = set()
        while True:
            key = terminal.inkey(0.001)
            if key: 
                keys.add(key)
            else:
                break
        return keys

    def log(self, message):
        """Write a log message. 
        Log messages are only shown when debug mode is on. 
        They can be very useful for debugging.

        Arguments:
            message (str): The message to log.
        """
        self.log_messages.append((self.turn_number, message))

    def end(self):
        """Ends the game. No more turns will run.
        """
        self.playing = False

    def add_agent(self, agent):
        """Adds an agent to the game.
        Whenever you want to add a new agent during the game, you must add it to 
        the game using this method.

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
        """Looks up an agent by name. 
        This is useful when one agent needs to interact with another agent.

        Arguments: 
            name (str): The agent's name. If there is no agent with this name, 
                you will get an error.

        Returns: 
            An agent.
        """
        validate_agent_name(name)
        if name in self.agents_by_name:
            return self.agents_by_name[name]
        else:
            raise AgentNotFoundByName(name)

    def is_empty(self, position):
        """Checks whether a position is occupied by any agents.

        Arguments: 
            position (int, int): The position to check.

        Returns: 
            A bool
        """
        return position not in self.get_agents_by_position()

    def get_agents_by_position(self):
        """Returns a dict where each key is a position (e.g. (10, 20)) and
        each value is a list containing all the agents at that position.
        This is useful when an agent needs to find out which other agents are
        on the same space or nearby.

        When called during ``play_turn()``, the dict reflects the board state
        at the start of the current agent's turn, including any moves made by
        agents that have already taken their turn this round.
        """
        if self._position_cache is not None:
            return self._position_cache
        positions = defaultdict(list)
        for agent in self.agents:
            if getattr(agent, "display", True):
                validate_position(agent.position)
                for pos in agent_occupied_positions(agent):
                    positions[pos].append(agent)
        self._position_cache = positions
        return positions

    def on_view(self, position):
        """Checks whether a position is within the current view.

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
        """Removes an agent from the game. 

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
        """Removes an agent from the game. 

        Arguments:
            name (str): the agent's name.
        """
        validate_agent_name(name)
        if name not in self.agents_by_name:
            raise AgentNotFoundByName(name)
        agent = self.agents_by_name.pop(name)
        self.agents.remove(agent)

    def on_board(self, position):
        """Checks whether a position is on the game board.

        Arguments: 
            position (int, int): The position to check

        Returns: 
            A bool
        """
        validate_position(position)
        x, y = position
        bx, by = self.board_size
        return x >= 0 and x < bx and y >= 0 and y < by



