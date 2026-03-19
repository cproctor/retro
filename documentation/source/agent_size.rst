.. _agent_size:

Extension: Multi-cell agents
=============================

By default, every agent takes up exactly one cell on the board — one character,
one position. That's all you need for most games. But sometimes you want an
agent that looks bigger: a spaceship that's three characters wide, or a boss
enemy that fills a 4×2 block. This extension shows you how.

This is completely optional. If your agents are single characters, you can
ignore this page entirely.

The idea
--------

Two things work together:

* ``size`` — a ``(width, height)`` tuple on your agent class, declaring how
  many cells the agent occupies.
* ``character`` — instead of a single character, a list of strings where each
  string is one row of the agent's appearance.

The agent's ``position`` is always the **top-left corner** of the agent.

A simple example
----------------

Here is a spaceship that takes up three columns and two rows::

    class BigShip:
        size = (3, 2)
        character = [
            " ^ ",
            "===",
        ]
        position = (10, 5)

On the board it looks like::

    ·········
    ·····^···
    ·····===·
    ·········

The ``^`` is at position ``(10, 5)`` (top-left), the ``=`` characters fill
the row below.

Collision detection
-------------------

When an agent has a ``size``, the game treats **every cell** it covers as
occupied. So :py:meth:`~retro.game.Game.is_empty` will return ``False`` for
any of those cells, and :py:meth:`~retro.game.Game.on_board` checks that
the entire agent fits on the board.

This means that if a small agent moves into any cell covered by a big agent,
``is_empty`` will catch it::

    new_pos = (11, 5)   # one cell to the right of BigShip's top-left
    if game.is_empty(new_pos):      # False — BigShip covers that cell
        self.position = new_pos

Keeping things on the board
----------------------------

When you call :py:meth:`~retro.game.Game.add_agent` or when an agent moves,
the game checks that every cell the agent occupies is within the board. If any
part of the agent hangs off the edge, you will get an error. Make sure the
agent's starting position (and any position it moves to) leaves enough room for
its full size.

For a ``size = (3, 2)`` agent on a board that is 25 columns wide, the
rightmost safe x position is ``22`` (so columns 22, 23, and 24 are all on the
board).

Character grid rules
---------------------

* The list of strings must not be taller than ``size[1]`` (the height).
* Each string must not be wider than ``size[0]`` (the width).
* Rows that are shorter than the width, or rows that are missing entirely,
  are filled with spaces.
* If you declare a ``size`` but give ``character`` a plain string, the string
  is displayed at the top-left cell and the rest of the space is blank.

If the character grid is *larger* than the declared size, the game raises a
``AgentCharacterTooLarge`` error right away so you can fix it.

Putting it together
--------------------

Here is a complete example of a two-row agent that can be moved with the arrow
keys::

    from retro.game import Game

    class Tank:
        size = (3, 2)
        character = [
            "[|]",
            "===",
        ]
        position = (10, 10)

        def handle_keystroke(self, keystroke, game):
            x, y = self.position
            if keystroke.name == "KEY_LEFT":
                new_pos = (x - 1, y)
            elif keystroke.name == "KEY_RIGHT":
                new_pos = (x + 1, y)
            elif keystroke.name == "KEY_UP":
                new_pos = (x, y - 1)
            elif keystroke.name == "KEY_DOWN":
                new_pos = (x, y + 1)
            else:
                return
            # Check that the whole tank stays on the board.
            # game.on_board checks the top-left corner; we also need to check
            # the bottom-right corner of the tank.
            bottom_right = (new_pos[0] + 2, new_pos[1] + 1)
            if game.on_board(new_pos) and game.on_board(bottom_right):
                self.position = new_pos

    tank = Tank()
    game = Game([tank], {}, board_size=(30, 20))
    game.play()

.. note::

    In the example above we manually check that the bottom-right corner stays
    on the board. A helper like ``game.on_board`` only tests a single point,
    so you need to verify the corners that are furthest from the top-left.
    A future version of Retro may add a convenience method for this.
