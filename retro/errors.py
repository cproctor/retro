class GameError(Exception):
    pass

class AgentWithNameAlreadyExists(GameError):
    def __init__(self, name):
        message = f"There is already an agent named {agent.name} in the game"
        super().__init__(message)

class AgentNotFoundByName(GameError):
    def __init__(self, name):
        message = f"There is no agent named {agent.name} in the game"
        super().__init__(message)

class AgentNotInGame(GameError):
    def __init__(self, agent):
        name = agent.name or f"anonymous {agent.__class__.__name__}"
        message = f"Agent {name} is not in the game"
        super().__init__(message)

class IllegalMove(GameError):
    def __init__(self, agent, position):
        name = agent.name or f"anonymous {agent.__class__.__name__}"
        message = f"Agent {name} tried to move to {position}"
        super().__init__(message)

class GraphError(GameError):
    pass

class TerminalTooSmall(GameError):
    BORDER_X = 2
    BORDER_Y = 3
    STATE_HEIGHT = 5

    def __init__(self, width=None, width_needed=None, height=None, height_needed=None):
        if width is not None and width_needed is not None and width_needed < width:
            err = f"The terminal width ({width}) is less than the required {width_needed}."
            super().__init__(err)
        elif height is not None and height_needed is not None and height_needed < height:
            err = f"The terminal height ({height}) is less than the required {height_needed}."
        else:
            raise ValueError(f"TerminalTooSmall called with illegal values.")
