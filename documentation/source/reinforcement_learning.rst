Reinforcement learning
======================

Once you have a working game, you can train a reinforcement learning (RL)
agent to play it automatically. The `retro-gamer
<https://pypi.org/project/retro-gamer/>`__ package is designed for exactly
this: it wraps any ``retro`` game in a training loop, uses deep Q-learning
to learn a policy, and provides tools to watch the trained agent play.

Full documentation is at https://docs.makingwithcode.org/retro-gamer.

Quick start
-----------

Install ``retro-gamer`` and create a training run for your game::

    pip install retro-gamer
    retro-gamer create --game my_game.py --output runs/my_game/
    retro-gamer train runs/my_game/

``retro-gamer`` reads your game's ``create_game()`` function automatically.
The only other requirement is a ``[tool.retro-gamer]`` section in your
project's ``pyproject.toml`` describing which keys the agent can press and
which game-state variable to use as the reward signal.

The ``autoplay`` convention
---------------------------

If your game module defines an ``autoplay()`` function, other tools — such as
``retro-console`` — can use it to run the game autonomously, for example as a
screen saver or demo mode.

``autoplay()`` should take no arguments and return a :py:class:`~retro.game.Game`
instance that is already configured to play itself, with no keyboard input
required. The simplest implementation loads a trained ``retro-gamer`` policy:

.. code-block:: python

    def autoplay():
        from retro_gamer import TrainedPolicy, PolicyInput
        ai = TrainedPolicy("runs/my_game/")
        game = create_game()
        game.input_source = PolicyInput(ai, game)
        return game

Tools that support the convention call ``autoplay()`` and then drive the
returned game with their own display loop::

    game = my_game_module.autoplay()
    game.start()
    while game.playing:
        game.step()

The convention is intentionally minimal: ``autoplay()`` is responsible only for
creating and configuring the game. Display, timing, and the main loop are left
to the caller. This lets the same ``autoplay()`` implementation work in a
terminal screen saver, a web renderer, or any other context.

.. note::

   The ``runs/my_game/`` path in the example above is a convention, not a
   requirement. You can store the training run anywhere and point
   ``TrainedPolicy`` at the right directory. If you are distributing a game
   with a bundled trained policy, consider placing the run directory inside
   your package and using :py:func:`importlib.resources` to locate it at
   runtime.
