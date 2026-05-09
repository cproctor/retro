from blessed.keyboard import Keystroke


class InputSource:
    def collect(self) -> set:
        raise NotImplementedError


class TerminalInput(InputSource):
    def __init__(self, terminal):
        self.terminal = terminal

    def collect(self) -> set:
        keys = set()
        while True:
            key = self.terminal.inkey(0.001)
            if key:
                keys.add(key)
            else:
                break
        return keys


class ProgrammaticInput(InputSource):
    def __init__(self):
        self._pending = None

    def press(self, key: str | None):
        """Queue a keystroke for the next turn. key is a name string like 'KEY_RIGHT' or 'q', or None."""
        self._pending = key

    def collect(self) -> set:
        key = self._pending
        self._pending = None
        if key is None:
            return set()
        return {_make_keystroke(key)}


def _make_keystroke(key_str: str) -> Keystroke:
    if key_str.startswith("KEY_"):
        return Keystroke(ucs='', code=None, name=key_str)
    return Keystroke(ucs=key_str, code=None, name=None)
