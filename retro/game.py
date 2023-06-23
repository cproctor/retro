from collections import defaultdict
from signal import signal, SIGWINCH
from blessed import Terminal
from retro.view import View
from retro.clock import Clock
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
    """
    STATE_HEIGHT = 5

    def __init__(self, agents, state, board_size=(64, 32), debug=False, framerate=24):
        self.log_messages = []
        self.agents_by_name = {}
        self.agents_by_position = defaultdict(list)
        self.state = validate_state(state)
        self.board_size = board_size
        self.debug = debug
        self.framerate = framerate
        self.clock = Clock(1/framerate)
        for agent in agents:
            self.add_agent(agent)

    def play(self):
        terminal = Terminal()
        with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
            view = View(terminal, self.board_size, self.debug)
            signal(SIGWINCH, view.render_layout)
            view.render_layout()
            for turn_number in self.clock.run():
                self.turn_number = turn_number
                for name, agent in sorted(self.agents_by_name.items()):
                    if hasattr(agent, 'play_turn'):
                        agent.play_turn(self)
                view.render(self)

    def log(self, message):
        self.log_messages.append((self.turn_number, message))

    def add_agent(self, agent):
        validate_agent(agent)
        if agent.name in self.agents_by_name:
            raise AgentAlreadyExists(agent.name)
        if not self.on_board(agent.position):
            raise IllegalMove(agent, agent.position)
        self.agents_by_name[agent.name] = agent
        self.agents_by_position[agent.position].append(agent)

    def get_agent_by_name(self, name):
        validate_agent_name(name)
        return self.agents_by_name[name]

    def get_agents_by_position(self, position):
        validate_position(position)
        return self.agents_by_position[position]

    def remove_agent_by_name(self, name):
        validate_agent_name(name)
        if name not in self.agents_by_name:
            raise AgentNotFound(name)
        agent = self.agents.pop(name)
        self.agents_by_position[agent.position].remove(agent)

    def move_agent(self, agent, position):
        validate_position(position)
        if not self.on_board(position):
            raise IllegalMove(agent, position)
        self.agents_by_position[agent.position].remove(agent)
        agent.position = position
        self.agents_by_position[agent.position].append(agent)

    def on_board(self, position):
        validate_position(position)
        x, y = position
        bx, by = self.board_size
        return x >= 0 and x < bx and y >= 0 and y < by



