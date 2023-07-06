Introduction
============

``Retro`` is a simple framework for creating Terminal-based games.

This introduction will guide you through how to create games using ``Retro``.
This introduction is meant for Python beginners, but you should know the basics 
of Object-Oriented programming, including how to define classes and create 
class instances. 

One way to think of a game is as a set of rules that all the players follow. 
Actually, let's talk about agents rather than players, because sometimes there
are characters in games which are not controlled by humans. In Retro, anything
that shows up on the game board will be an agent, even if it just sits there
for the whole game and doesn't do anything. 

The hardest part of creating a game is designing it. Consider the following:

* Which genre? Action? Puzzle? Narrative? Artistic?
* What's the goal? (Is there a goal?)
* What will the board look like? 
* How will the user interact with the game?

Dream big, but start small. What would be the smallest, simplest version of your game? 
Start with that.

Games
-----

Retro contains one main class that you'll use to create games: :py:class:`~retro.game.Game`.
When you create an instance of :py:class:`~retro.game.Game`, there are two required arguments:

* A list of agents
* A dict representing the initial game state.

Here's a very simple game, using the built-in :py:class:`~retro.agent.ArrowKeyAgent`::

    from retro.game import Game
    from retro.agent import ArrowKeyAgent
    
    agent = ArrowKeyAgent()
    state = {}
    game = Game([agent], state)
    game.play()

To run this game, copy the code above into a file and run it. Or just run::

    python -m retro.examples.simple

A game can also be run in debug mode by using the optional argument ``debug=True``
when creating a :py:class:`~retro.game.Game`. When a game runs in debug mode, you will
see a sidebar containing log messages, including when there are keystrokes and 
anytime the code invokes :py:meth:`retro.game.Game.log`. Test out debug mode 
using::

    python -m retro.examples.debug

The game loop
+++++++++++++

Every game you write will use the same :py:class:`~retro.game.Game` class.
A game's uniqueness comes from the agents it includes. Here is an overview
of how agents work within a game:

The game runs as a series of turns. Each turn:

* Each agent's :py:meth:`~retro.agent.Agent.handle_keystroke` method is called
  for each keystroke which has been entered since the last turn
  (if the agent has this method).
* Each agent's :py:meth:`~retro.agent.Agent.play_turn` method is called
  (if the agent has this method).
* In either of these methods, the agent may change its character, position, or color. 
  The agent also receives the current :py:class:`~retro.game.Game` as an argument in both 
  methods, so it can look up properties of the game, access other agents, or 
  change the game's state. 
* Then the game draws the board, displaying each agent's character at its position, 
  in its color. The game also prints out its current state. 

The game ends once :py:meth:`retro.game.Game.end` is called.

Agents
++++++

An agent is an instance of a class which has attributes and methods similar to 
:py:class:`~retro.agent.Agent`. The 
:py:attr:`~retro.agent.Agent.character`,
:py:attr:`~retro.agent.Agent.position`, and 
:py:attr:`~retro.agent.Agent.color` attributes determine how and where the agent
is displayed on the game board. The 
:py:meth:`~retro.agent.Agent.handle_keystroke` and 
:py:meth:`~retro.agent.Agent.play_turn` methods determine the agent's behavior 
within the game. 

Example: Nav
------------

::

   ╔═════════════════════════╗
   ║       O                 ║
   ║ O                      O║
   ║      O                  ║
   ║                         ║
   ║                         ║
   ║                         ║
   ║  O                      ║
   ║                         ║
   ║  O                O     ║
   ║             O           ║
   ║O                        ║
   ║                         ║
   ║                 OO      ║
   ║          O              ║
   ║        O                ║
   ║                  O      ║
   ║                         ║
   ║                O        ║
   ║       O                 ║
   ║                         ║
   ║          O  O           ║
   ║            O            ║
   ║                         ║
   ║  O         O            ║
   ║ O             ^         ║
   ╠═════════════════════════╣
   ║score: 408               ║
   ║                         ║
   ║                         ║
   ║                         ║
   ╚═════════════════════════╝

For this example, we're going to create a simple game in which you are flying 
a spaceship through a field of asteroids. It's a simple action game; you've probably
played something like it before. You can play our version by running::

    python -m retro.examples.nav

We need to write a few different agent classes to implement this game. First, we'll 
need a spaceship::

    from retro.game import Game

    HEIGHT = 25
    WIDTH = 25

    class Spaceship:
        name = "ship"
        character = '^'
        position = (WIDTH // 2, HEIGHT - 1)

        def handle_keystroke(self, keystroke, game):
            x, y = self.position
            if keystroke.name in ("KEY_LEFT", "KEY_RIGHT"):
                if keystroke.name == "KEY_LEFT": 
                    new_position = (x - 1, y)
                else: 
                    new_position = (x + 1, y)
                if game.on_board(new_position):
                    if game.is_empty(new_position):
                        self.position = new_position
                    else:
                        game.end()

    ship = Spaceship()
    game = Game([ship], {"score": 0}, board_size=(WIDTH, HEIGHT))
    game.play()

Spaceship is a pretty simple class. The ship's character is ``^``, 
its position starts at the bottom center of the screen, and when the 
left or arrow key is pressed, it moves left or right. If the ship's new position
is empty, it moves to that position. If the new position is occupied (by an asteroid!)
the game ends. Save the code above in a new file and run it. Currently the game
never ends, so press ``Control+C`` when you get tired of moving the spaceship around.

Now we need some asteroids to avoid. We can write one Asteroid class, and then 
create as many instances as we need. But who will create new Asteroids? 
We will also write an AsteroidSpawner class, which is not displayed on the board
but which constantly spawns asteroids. Let's write Asteroid first::

    class Asteroid:
        character = 'O'
    
        def __init__(self, position):
            self.position = position
    
        def play_turn(self, game):
            if game.turn_number % 2 == 0: 
                x, y = self.position
                if y == HEIGHT - 1: 
                    game.remove_agent_by_name(self.name)
                else:
                    ship = game.get_agent_by_name('ship')
                    new_position = (x, y + 1)
                    if new_position == ship.position:
                        game.end()
                    else:
                        self.position = new_position

There are a few details to note here. 
First, Asteroid doesn't have a position; the AsteroidSpawner will
decide on the Asteroid's initial position and pass it in to 
Asteroid's :py:meth:`~retro.examples.nav.Asteroid.__init__` method.

In :py:meth:`~retro.examples.nav.Asteroid.play_turn`, nothing happens unless
``game.turn_number`` is divisible by 2. The result is that asteroids only move 
on even-numbered turns. (This is a good strategy for when you want some agents to
move more slowly than others.) Now, if the asteroid is at the bottom of the screen, 
it has run its course and should be removed from the game. Otherwise, the asteroid's
new position is one space down from its old position. If the asteroid's new position 
is the same as the ship's position, the game ends. 

Add the Asteroid class to your game file, and edit the code at the bottom of the file 
to add an Asteroid to the game::

    ship = Spaceship()
    asteroid = Asteroid((WIDTH // 2, 0))
    game = Game([ship, asteroid], {"score": 0}, board_size=(WIDTH, HEIGHT))
    game.play()

Your code should now look like this ::ref:`asteroid_v1`. Test it out a few times.

But we want lots of asteroids! Let's write another agent class for an AsteroidSpawner, 
which will possibly spawn an asteroid each turn::

    class AsteroidSpawner:
        display = False
    
        def play_turn(self, game):
            game.state['score'] += 1
            if self.should_spawn_asteroid(game.turn_number):
                asteroid = Asteroid((randint(0, WIDTH - 1), 0))
                game.add_agent(asteroid)
    
        def should_spawn_asteroid(self, turn_number):
            return randint(0, 1000) < turn_number

On each turn, :py:class:`~retro.examples.nav.AsteroidSpawner` 
adds 1 to the game score and then uses 
:py:meth:`~retro.examples.nav.should_spawn_asteroid` to decide whether to 
spawn an asteroid, using a simple but effective algorithm to make the game get
progressively more difficult: choose a random 
number and return ``True`` if the number is less than the current turn number. 
At the beginning of the game, few asteroids will be spawned. As the turn number
climbs toward 1000, asteroids are spawned almost every turn. 

When :py:meth:`~retro.examples.nav.should_spawn_asteroid` comes back ``True``, 
:py:class:`~retro.examples.nav.AsteroidSpawner` creates a new instance of 
:py:class:`~retro.examples.nav.Asteroid` at a random position along the top of 
the screen and adds the asteroid to the game. 

Add :py:class:`~retro.examples.nav.AsteroidSpawner` to your game file and update the 
code at the bottom::

    ship = Spaceship()
    spawner = AsteroidSpawner()
    state = {"score": 0}
    game = Game(
        [ship, spawner],
        state
        board_size=(WIDTH, HEIGHT)
    )
    game.play()

You should have a fully-functioning game. The full 

.. toctree::
   :maxdepth: 1

   nav_v1
   nav
   snake
