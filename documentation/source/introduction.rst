Introduction
============

This introduction will guide you through how to create games using ``Retro``.
This introduction is meant for Python beginners, but you should know the basics 
of Object-Oriented programming, including how to define classes and create 
class instances. 

One way to think of a game is as a set of rules that all the players follow. 
Actually, let's talk about agents rather than players, because sometimes there
are characters in games which are not controlled by humans. In Retro, anything
that shows up on the game board will be an agent, even if it just sits there
for the whole game and doesn't do anything. 

To create a game, start by drawing what the board will look like. 
To create a game in Retro, all you need to do is to define the agents in the game.
You will write a class for each kind of agent in your game.

.. toctree::
   :maxdepth: 1

   snake
