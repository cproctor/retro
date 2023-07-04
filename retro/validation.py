
def validate_agent(agent):
    if not hasattr(agent, "name"):
        raise ValueError(f"Agent {agent} must have a name")
    if getattr(agent, 'display', True):
        validate_position(agent.position)
        if not hasattr(agent, "character"):
            raise ValueError(f"Agent {agent.name} must have a character")

    validate_agent_name(agent.name)
    return agent

def validate_state(state):
    if not isinstance(state, dict):
        raise TypeError(f"State is {type(state)}, but must be a dict.")
    for key, value in state.items():
        if is_mutable(value):
            raise ValueError(f"State must be immutable, but state[{key}] is {value}")
    return state

def validate_agent_name(name):
    if not isinstance(name, str):
        raise TypeError(f"Agent names must be strings")
    return name

def validate_position(position):
    if not isinstance(position, tuple):
        raise TypeError(f"Position is {type(position)}, but must be a tuple.")
    if not len(position) == 2:
        raise ValueError(f"Position is {position}. Must be a tuple of two integers.")
    if not isinstance(position[0], int) and isinstance(position[1], int):
        raise TypeError(f"Position is {position}. Must be a tuple of two integers.")
    return position
    
def is_mutable(obj):
    if isinstance(obj, (int, float, bool, str, None)):
        return False
    elif isinstance(obj, tuple):
        return all(is_mutable(element) for element in obj)
    else:
        return True





