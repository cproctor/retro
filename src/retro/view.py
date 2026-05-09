# Compatibility shim — import from the new location instead.
from retro.views.terminal import TerminalView as View
from retro.views._util import get_agent_character

__all__ = ["View", "get_agent_character"]
