# Retro

A simple framework for Terminal-based games.

```
╔════════════════════════════════╗
║                                ║
║                                ║
║                                ║
║      *************             ║
║      *                         ║
║      *                         ║
║      **>                       ║
║             @                  ║
║                                ║
║                                ║
╠════════════════════════════════╣
║score: 153                      ║
║                                ║
╚════════════════════════════════╝
```

## Layout

- There are two panes, a fixed-size play area at the top and a state window
  at the bottom. When enabled, a sidebar containing debug messages is also shown.

## Concepts and skills needed

- We need to discuss immutability, and the difference between 
  mutable objects and immutable values. 
  - Specifically, we care about the difference between tuples and lists.
  - State must be immutable!
  - Objects are only ever equal to themselves.

- The game is structured as a collection of agents which interact.

## Design/pedagogical criteria

- Make thinking visible.
  - Avoid subclasses; they require interaction with invisible parent attributes.
  - Instead, compose functionality from other classes which might be somewhat black-boxed.
