import miniworldmaker.tokens.token as board_token
from miniworldmaker.boards import board_position


class Actor(board_token.Token):
    """ Initializes a new actor

    An actor is a specialized Token:

    In contrast to a token, an actor has an act method and its own event handlers (key_pressed, mouse_pressed, ...)
    and is therefore active itself in contrast to the token, which must always be controlled by the board.

    Args:
        position: The position on the board as tuple.
        If None, the actor will not be placed on the board.

    Examples:

        Usually you create your own subclass of Actor:

        >>> class Player(Actor):
        >>>     def __init__(self, position):
        >>>         super().__init__(position)
        >>>
        >>>
        >>> class MyBoard(PixelBoard):
        >>>     def __init__(self):
        >>>         self.player = Player(position = (100,60))
        >>>
        >>> # Add Actor methods to any token class.
        >>> class MyRectangle(Rectangle, Actor)
        >>>     pass
    """

    def __init__(self, position=None):
        super().__init__(position)
        self._orientation = 0
        self.registered_event_handlers["mouse_left"] = self.on_mouse_left
        self.registered_event_handlers["mouse_right"] = self.on_mouse_left
        self.registered_event_handlers["mouse_motion"] = self.on_mouse_motion
        self.registered_event_handlers["key_pressed"] = self.on_key_pressed
        self.registered_event_handlers["key_down"] = self.on_key_down
        self.registered_event_handlers["key_up"] = self.on_key_up
        self.on_setup()

    def add_to_board(self, board, position: board_position.BoardPosition):
        super().add_to_board(board, position)

    def on_key_pressed(self, keys):
        """
        Gets all pressed keys

        Args:
            keys: Gets all currently pressed keys as list.

        """
        pass

    def on_key_up(self, keys):
        """
        Is called, when key is pressed down. Gets all pressed keys

        Args:
            keys: Gets all currently pressed keys as list.

        """
        pass

    def on_key_down(self, keys):
        """
        Is called, when key is released. Gets all pressed keys

        Args:
            keys: Gets all currently pressed keys as list.

        """
        pass

    def on_mouse_left(self, mouse_pos):
        """
        Is called, when mouse_left is pressed

        Args:
            mouse_pos: The mouse_position

        """
        pass

    def on_mouse_right(self, mouse_pos):
        """
        Is called, when mouse_right is pressed

        Args:
            mouse_pos: The mouse_position

        """
        pass

    def on_mouse_motion(self, mouse_pos):
        """
        Is callen, when mouse is moved

        Args:
            mouse_pos: The mouse position

        """
        pass

    def on_setup(self):
        """
        Is called, when object is created.

        """
        pass

    def act(self):
        """
        Is called every frame.

        """
        pass

    def __str__(self):
        actor_string = super().__str__()
        if self.board:
            actor_string = actor_string + " with Direction: {0}".format(self.direction)
        return actor_string
