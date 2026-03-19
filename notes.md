What needs to be done

- There is some case where `retro.errors.TerminalTooSmall` gets called with illegal values. 
  Find the error, fix it, and add tests.
- When the game is no longer playing, assign a keystroke to exit the program.


How would I implement the "shadow game"?

- One thing we know ahead of time is that agents update their positions, and it's up to the game
  to query 

- Keep a per-agent dict of positions. 

When have agent positions changed?
- When any agent position changes
- When any agent is added
- When any agent is removed
