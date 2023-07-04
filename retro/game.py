from collections import defaultdict
from signal import signal, SIGWINCH
from time import sleep
from blessed import Terminal
from retro.view import View
from retro.validation import (
    validate_agent, 
    validate_state,
    validate_agent_name,
    validate_position,
)
from retro.errors import (
    AgentAlreadyExists,
    AgentNotFound,
    IllegalMove,
)

class Game:
    """
    Creates a playable game.
    You will use Game to create games, but don't need to read or understand how
    this class works. The main work in creating a 

    Arguments: 
        agents (list): A list of Agents to add to the game. 
        state (dict): A dict containing the game's initial state. 
        board_size (int, int): (Optional) The two-dimensional size of the game board. D
        debug (bool): (Optional) Turn on debug mode, showing log messages while playing.
        framerate (int): (Optional) The target number of frames per second at which the 
            game should run.

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

    def __init__(self, agents, state, board_size=(64, 32), debug=False, framerate=24):
        self.log_messages = []
        self.agents_by_name = {}
        self.agents = []
        self.state = validate_state(state)
        self.board_size = board_size
        self.debug = debug
        self.framerate = framerate
        self.turn_number = 0
        for agent in agents:
            self.add_agent(agent)

    def play(self, color='white_on_black'):
        """Starts the game.

        Arguments:
            color (str): (Optional) The game's background color scheme. `Available colors <https://blessed.readthedocs.io/en/latest/colors.html>`_.
        """
        self.playing = True
        terminal = Terminal()
        with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
            view = View(terminal, color=color)
            while self.playing:
                self.turn_number += 1
                self.keys_pressed = self.collect_keystrokes(terminal)
                if self.debug and self.keys_pressed:
                    self.log("Keys: " + ', '.join(k.name or str(k) for k in self.keys_pressed))
                for name, agent in sorted(self.agents_by_name.items()):
                    if hasattr(agent, 'handle_keystroke'):
                        for key in self.keys_pressed:
                            agent.handle_keystroke(key, self)
                    if hasattr(agent, 'play_turn'):
                        agent.play_turn(self)
                    if getattr(agent, 'display', True):
                        if not self.on_board(agent.position):
                            raise IllegalMove(agent, agent.position)
                view.render(self)
            while True:
                if terminal.inkey().name in self.EXIT_CHARACTERS:
                    break

    def collect_keystrokes(self, terminal):
        keys = set()
        while True:
            key = terminal.inkey(0.01)
            if key: 
                keys.add(key)
            else:
                break
        sleep(1/self.framerate)
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
        """Adds an Agent to the game.
        Whenever you want to add a new agent during the game, you must add it to 
        the game using this method.

        Arguments: 
            agent: An instance of an agent class. 
        """
        validate_agent(agent)
        if agent.name in self.agents_by_name:
            raise AgentAlreadyExists(agent.name)
        if getattr(agent, "display", True) and not self.on_board(agent.position):
            raise IllegalMove(agent, agent.position)
        self.agents_by_name[agent.name] = agent
        self.agents.append(agent)

    def get_agent_by_name(self, name):
        """Looks up an agent by name. 
        This is useful when one agent needs to interact with another agent.

        Arguments: 
            name (str): The Agent's name. If there is no agent with this name, 
                you will get an error.

        Returns: 
            An Agent.
        """
        validate_agent_name(name)
        return self.agents_by_name[name]

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
        each value is a list containing all the Agents at that position.
        This is useful when an Agent needs to find out which other Agents are
        on the same space or nearby.
        """
        positions = defaultdict(list)
        for agent in self.agents:
            if getattr(agent, "display", True):
                validate_position(agent.position)
                positions[agent.position].append(agent)
        return positions

    def remove_agent_by_name(self, name):
        """Removes an Agent from the game. 

        Arguments:
            name (str): the Agent's name.
        """
        validate_agent_name(name)
        if name not in self.agents_by_name:
            raise AgentNotFound(name)
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



