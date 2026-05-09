def get_agent_character(agent, position):
    """Returns the character to display for an agent at the given board position.
    For agents with a multi-row character grid, returns the character for that cell.
    """
    char = agent.character
    if isinstance(char, str) or not hasattr(agent, 'size'):
        return char
    ax, ay = agent.position
    x, y = position
    dx, dy = x - ax, y - ay
    rows = list(char)
    if dy >= len(rows):
        return ' '
    row = rows[dy]
    if dx >= len(row):
        return ' '
    return row[dx]
