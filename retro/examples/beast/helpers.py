def add(vec0, vec1):
    """Adds two vectors.
    Got tired of doing this by hand. 
    """
    x0, y0 = vec0
    x1, y1 = vec1
    return (x0 + x1, y0 + y1)

def get_occupant(game, position):
    """Returns the agent at position, if there is one. 
    This function slightly simplifies the process of getting the 
    agent at a position: the game returns a list of agents at a position, 
    because some games allow more than one agent at a position.
    """
    positions_with_agents = game.get_agents_by_position()
    if position in positions_with_agents:
        agents_at_position = positions_with_agents[position]
        return agents_at_position[0]

def distance(vec0, vec1):
    """Returns the distance between two vectors, using the
    "manhattan distance," or the distance if you can only 
    move in the x-direction or the y-direction, but not 
    diagonally. Just like walking blocks in Manhattan :)
    """
    x0, y0 = vec0
    x1, y1 = vec1
    return abs(x1 - x0) + abs(y1 - y0)

