class Agent:
    """Represents a character in the game. To create an Agent, define a new
    class with some of the attributes and methods below. You may change any of
    the Agent's attributes at any time, and the result will immediately be 
    visible in the game.

    After you create your Agents, add them to the ``Game``, either when it is created
    or using ``Game.add_agent`` later on. Then the Game will take care of calling 
    the Agent's methods at the appropriate times. 

    Attributes:
        character: (Required) A one-character string which will be displayed 
            at the Agent's position on the game board. 
        position: (Required) The character's ``(int, int)`` position on the game
            board. 
        name: (Optional) If an agent has a name, it must be unique within the game. 
            Agent names can be used to look up agents with 
            :py:meth:`retro.game.Game.get_agent_by_name`. 
        display: (Optional) When ``False``, the Agent will not be displayed on the 
            board. This is useful when you want to create an agent which will be displayed
            later, or when you want to create an agent which acts on the Game indirectly, 
            for example by spawning other Agents. Defaults to True.
        z: (Optional) When multiple Agents have the same position on the board, the 
            Agent with the highest ``z`` value will be displayed. 
            The Game is played on a two-dimensional (x, y) board, but you can think of 
            ``z`` as a third "up" dimension. Defaults to 0.
    """
    character = "*"
    position = (0, 0)
    name = "agent"
    display = True
    z = 0

    def play_turn(self, game):
        """If an Agent has this method, it will be called once 
        each turn. 

        Arguments: 
            game (Game): The game which is currently being played will be 
                passed to the Agent, in case it needs to check anything about
                the game or make any changes. 
        """
        pass

    def handle_keystroke(self, keystroke, game):
        """If an Agent has a this method, it will be called every
        time a key is pressed in the game.

        Arguments: 
            keystroke (blessed.keyboard.Keystroke): The key which was pressed. You can 
                compare a Keystroke with a string (e.g. ``if keystroke == 'q'``) to check 
                whether it is a regular letter, number, or symbol on the keyboard. You can 
                check special keys using the keystroke's name 
                (e.g. ``if keystroke.name == "KEY_RIGHT"``). Run your game in debug mode to 
                see the names of keystrokes. 
            game (Game): The game which is currently being played will be 
                passed to the Agent, in case it needs to check anything about
                the game or make any changes. 
            
        """
        pass

class ArrowKeyAgent:
    """A simple agent which can be moved around with the arrow keys.
    """
    name = "ArrowKeyAgent"
    character = "*"
    position = (0,0)
    display = True
    z = 0

    def play_turn(self, game):
        pass

    def handle_keystroke(self, keystroke, game):
        """Moves the agent's position if the keystroke is one of the arrow keys.
        One by one, checks the keystroke's name against each arrow key. 
        Then uses :py:meth:`try_to_move` to check whether the move is on the 
        game's board before moving.
        """
        x, y = self.position
        if keystroke.name == "KEY_RIGHT":
            self.try_to_move((x + 1, y), game)
        elif keystroke.name == "KEY_UP":
            self.try_to_move((x, y - 1), game)
        elif keystroke.name == "KEY_LEFT":
            self.try_to_move((x - 1, y), game)
        elif keystroke.name == "KEY_DOWN":
            self.try_to_move((x, y + 1), game)

    def try_to_move(self, position, game):
        """Moves to the position if it is on the game board. 
        """
        if game.on_board(position):
            self.position = position
            game.log(f"Position: {self.position}")
