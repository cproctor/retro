from typing import Protocol, runtime_checkable

from retro.views.terminal import TerminalView
from retro.views.headless import HeadlessView


@runtime_checkable
class View(Protocol):
    def on_game_start(self, game) -> None: ...
    def render(self, game) -> None: ...


__all__ = ["View", "TerminalView", "HeadlessView"]
