class GameError(Exception):
    pass

class AgentAlreadyExists(GameError):
    def __init__(self, name):
        message = f"There is already an agent named {agent.name} in the game"
        super().__init__(message)

class AgentNotFound(GameError):
    def __init__(self, name):
        message = f"There is no agent named {agent.name} in the game"
        super().__init__(message)

class IllegalMove(GameError):
    def __init__(self, agent, position):
        message = f"Agent {agent.name} tried to move to {position}"
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
