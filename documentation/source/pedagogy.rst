Pedagogy
========

Superturtle is part of the `Making With Code (MWC)` introductory computer science
curriculum, with an intended audience of beginners. If you are interested 
in `Making With Code`, or if you found `Retro` helpful, 
`Dr. Chris Proctor <https://chrisproctor.net>`_ would love to hear from you. 

Design
------

Our primary goal in developing Retro was to provide a platform for open-ended 
game creation which would be manageable for beginning CS students learning about
Object-Oriented programming for the first time. Scratch does this wonderfully, and 
we love Scratch, but `MWC` is aiming for a different relationship with code. 

In previous versions of `MWC`, we used :doc:`quest:index`, a library which provides
a simplifled wrapper around :doc:`arcade:index`. However, we found that Quest was
still too complex for most students. A few specific issues:

- Quest follows PyArcade's design pattern of relying heavily on class inheritance to 
  compose functionality. This can be a terse and graceful approach, but it makes 
  comprehension, implementation, and debugging difficult for beginners. We wanted an approach 
  where code is either fully visible (implementation of agents) or abstracted away
  (:py:class:`~retro.game.Game`).
- GUI-based games invite students to compare their projects with releases from game
  studios which employ hundreds or thousands of professionals, leading to unrealistic
  aspirations and disappointment. Students sometimes spent too much time designing
  maps and sprites. With a character-based array, Retro is obviously very constrained; 
  within these constraints, students are challenged to eke out as much expressiveness
  as they can.
- The simplicity of discrete integer-indexed positions within an array of characters, 
  and a one-to-one mapping between agents and characters on the board supports 
  conceptual understanding of class instances.
- A debugging mode is provided.

Teaching with Retro
-------------------

This section needs to be written up more fully; these are just notes.

- Make sure students already have some practice with classes and instances. MWC's 
  Unit 3 provides this support. 
- Support students in designing their games, including teacher sign-off on a planning 
  document. (Provide planning sheets of grid paper in the aspect ratio of Terminal 
  characters (generally, around 1x2).
- Model how to use the debugging mode, including logging, stepping through turns 
  by slowing the framerate, 
- Retro is well-suited to indy-style games which get away from stereotypical 
  "men shooting each other in the head" games. Look at examples together to help students
  expand their imaginations of what kinds of games they might want to make.



