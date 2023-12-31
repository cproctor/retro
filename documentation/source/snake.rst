.. _snake:

Extended example: Snake
=======================

Here's a longer example, a classic game where you guide a snake around the board, 
searching for delicious apples. Every time you eat an apple you grow longer, until 
it's hard to stay out of your own way. 

Before we go any further, try out the game::

    $ python -m retro.examples.snake

Think about which agents we'll need in this game: 

* We need an apple. One will be enough; whenever the snake catches the apple, 
  we can have it move to a new location.
* We also need a snake. But the snake needs more than one character, and needs 
  to grow as more apples are eaten. We can accomplish this by creating two different
  kinds of Agents: a SnakeHead and a SnakeBodySegment. 

Now we will go through these Agents one by one. Read the documentation below to get an
overview of how the class works, and then click ``[source]`` to read the source code. 

Apple 
-----

.. autoclass:: retro.examples.snake.Apple
   :members:

SnakeHead
---------

.. autoclass:: retro.examples.snake.SnakeHead
   :members:

SnakeBodySegment
----------------

.. autoclass:: retro.examples.snake.SnakeBodySegment
   :members:



