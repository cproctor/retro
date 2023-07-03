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
    """
    STATE_HEIGHT = 5

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

    def play(self):
        self.playing = True
        terminal = Terminal()
        with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
            view = View(terminal)
            while self.playing:
                self.turn_number += 1
                self.keys_pressed = self.collect_keystrokes(terminal)
                if self.debug and self.keys_pressed:
                    self.log("Keys: " + ', '.join(k.name or str(k) for k in self.keys_pressed))
                for name, agent in sorted(self.agents_by_name.items()):
                    for key in self.keys_pressed:
                        agent.handle_keystroke(key, self)
                    if hasattr(agent, 'play_turn'):
                        agent.play_turn(self)
                view.render(self)

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
        self.log_messages.append((self.turn_number, message))

    def end(self):
        self.playing = False

    def add_agent(self, agent):
        validate_agent(agent)
        if agent.name in self.agents_by_name:
            raise AgentAlreadyExists(agent.name)
        if not self.on_board(agent.position):
            raise IllegalMove(agent, agent.position)
        self.agents_by_name[agent.name] = agent
        self.agents.append(agent)

    def get_agent_by_name(self, name):
        validate_agent_name(name)
        return self.agents_by_name[name]

    def get_agents_by_position(self):
        positions = defaultdict(list)
        for agent in self.agents:
            validate_position(agent.position)
            positions[agent.position].append(agent)
        return positions

    def remove_agent_by_name(self, name):
        validate_agent_name(name)
        if name not in self.agents_by_name:
            raise AgentNotFound(name)
        agent = self.agents.pop(name)
        self.agents_by_position[agent.position].remove(agent)

    def on_board(self, position):
        validate_position(position)
        x, y = position
        bx, by = self.board_size
        return x >= 0 and x < bx and y >= 0 and y < by



