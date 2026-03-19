.. _large_boards:

Extension: Large boards and scrolling views
============================================

By default, the game board and the view are the same size — everything on the
board is always visible on screen. But what if you want a board that is much
larger than what fits on the screen? Think of a maze that stretches far beyond
the edges of the terminal, or a world the player can explore by moving through
it.

This is an optional extension. If your game fits comfortably on one screen, you
can skip this entirely. If you want to build something bigger, read on.

The idea
--------

When you create a :py:class:`~retro.game.Game`, you can set two sizes
independently:

* ``board_size`` — how large the game world actually is.
* ``view_size`` — how much of it is visible on screen at once.

The visible portion is called the **view**. The view has a position on the
board, called the **view position**, which is the board coordinate of the
view's top-left corner. By changing ``game.view_position`` during the game,
you can scroll the view around the board.

.. code-block::

   Board (400 × 200)
   ┌────────────────────────────────────────────────────────┐
   │                                                        │
   │         ┌──────────────────┐                          │
   │         │  View (40 × 20)  │                          │
   │         │                  │                          │
   │         │        *         │                          │
   │         │                  │                          │
   │         └──────────────────┘                          │
   │                                                        │
   └────────────────────────────────────────────────────────┘

Only agents inside the view are drawn on screen. Agents outside the view still
exist and still take their turns — they just aren't visible.

Setting up a large board
------------------------

Pass both ``board_size`` and ``view_size`` when creating the game::

    from retro.game import Game

    game = Game(
        agents,
        state,
        board_size=(400, 200),
        view_size=(40, 20),
    )

You can also set the initial view position with ``view_position``::

    game = Game(
        agents,
        state,
        board_size=(400, 200),
        view_size=(40, 20),
        view_position=(180, 90),   # start near the center of the board
    )

Moving the view
---------------

During the game, any agent can move the view by setting
``game.view_position`` to a new ``(x, y)`` coordinate::

    def play_turn(self, game):
        # scroll the view one step to the right
        vx, vy = game.view_position
        game.view_position = (vx + 1, vy)

You can also check whether a position is currently visible using
:py:meth:`~retro.game.Game.on_view`::

    if game.on_view(self.position):
        game.log("I'm on screen!")

CenterViewAgent
---------------

The most common thing to want is for the view to follow the player around the
board, keeping the player centered on screen. The built-in
:py:class:`~retro.agent.CenterViewAgent` mixin does exactly this.

To use it, add ``CenterViewAgent`` as a second base class alongside whatever
other class your player inherits from::

    from retro.agent import ArrowKeyAgent, CenterViewAgent

    class Player(ArrowKeyAgent, CenterViewAgent):
        character = "*"
        color = "red_on_black"

        def __init__(self, position):
            self.position = position

On every turn, :py:class:`~retro.agent.CenterViewAgent` will adjust
``game.view_position`` so that the player stays in the center of the view.

**Using a margin**

Re-centering the view on every single turn can feel a bit jittery — the view
shifts even if the player only moves one step. If you'd prefer the view to only
re-center when the player gets close to the edge, set a ``margin``::

    class Player(ArrowKeyAgent, CenterViewAgent):
        character = "*"
        margin = 5            # re-center when within 5 spaces of any edge

With ``margin = 5``, the view stays still while the player is comfortably in
the middle, and only snaps back to center when the player gets within five
spaces of the edge.

Putting it together: a labyrinth
---------------------------------

Here is a complete example of a game that uses a large board with a scrolling
view. The player navigates a maze looking for the goal. Try it::

    python -m retro.examples.labyrinth

The key parts are the board and view sizes in the game setup::

    WIDTH, HEIGHT = 400, 200
    VIEW_WIDTH, VIEW_HEIGHT = 40, 20

    game = Game(
        [player] + maze.get_agents(),
        state,
        board_size=(WIDTH, HEIGHT),
        view_size=(VIEW_WIDTH, VIEW_HEIGHT),
    )

And the ``Player`` class, which inherits from both
:py:class:`~retro.agent.ArrowKeyAgent` and
:py:class:`~retro.agent.CenterViewAgent` to get arrow-key movement and
automatic view-following for free:

.. autoclass:: retro.examples.labyrinth.player.Player
   :members:

API reference
-------------

.. automethod:: retro.game.Game.on_view

.. autoclass:: retro.agent.CenterViewAgent
   :members:
