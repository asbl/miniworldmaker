from __future__ import annotations

from typing import List

import miniworldmaker.appearances.costume as costume_mod
import miniworldmaker.base.app as app
import miniworldmaker.boards.board_templates.pixel_board.board as board_mod
import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import (
    NotImplementedOrRegisteredError,
)


class Meta(type):
    def __call__(cls, *args, **kwargs):
        if len(args) >= 2 and type(args[0]) == int and type(args[1]) == int:
            first = (args[0], args[1])
            last_args = [args[n] for n in range(2, len(args))]
            args = [first] + last_args
        instance = type.__call__(cls, *args, **kwargs)  # create a new Token
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board()
        return instance


class BaseToken(pygame.sprite.DirtySprite, metaclass=Meta):

    def __init__(self, board=None):
        self._dirty = 0  # must be set before calling __init__ of DirtySprite.
        self.is_display_initialized: bool = False
        super().__init__()
        if not board:
            self._board: "board_mod.Board" = app.App.running_board
        else:
            self.board = board
        self._position = (0, 0)

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board):
        self.set_board(new_board)

    def set_board(self, new_board):
        if not self._board:
            self._board = new_board
        elif not new_board:
            pass
        else:
            _token_connector = new_board.get_token_connector(self)
            _token_connector.switch_board(new_board)

    def new_costume(self):
        return self.board.get_token_connector(self).create_costume()

    def get_costume_class(self) -> type["costume_mod.Costume"]:
        return self.board.get_token_connector(self).get_token_costume_class()

    @property
    def dirty(self) -> int:
        """If token is dirty, it will be repainted.

        Returns:

            int: 1 if token is dirty/0 otherwise
        """
        return self._dirty

    @dirty.setter
    def dirty(self, value: int):
        if self.position_manager and (
                self.board and
                self.board.camera.is_token_repainted(self)) and value == 1:
            self._dirty = 1
        elif value == 0:
            self._dirty = 0
        else:
            pass

    @property
    def rect(self) -> pygame.Rect:
        """Implemented in subclass
        """
        pass

    @property
    def image(self) -> pygame.Surface:
        """Implemented in subclass
        """
        return self.costume_manager.image

    def on_detecting_token(self, token: "Token"):
        """*on_sensing_token* is called, when token is sensing a token on same position

        Args:
            token (Token): The found token

        Examples:

            Register sensing_token event

            .. code-block::

                @player.register
                def on_sensing_token(self, token):
                    print("Player 1: Sensing token:")
                    if token == player2:
                    print("Am i sensing player2?" + str(token == player2))

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_detecting_token)

    # on_touching_token = on_sensing_token @todo: replace or add listeneer

    def is_detecting_board(self, distance: int = 0) -> bool:
        """
        Is the token on board if it is moving distance steps forward?

        .. image:: ../_images/sensing_on_board.png

        Args:
            distance: Specifies the distance in front of the actuator to which the sensors reacts.

        Returns:
            True if token is on board

        """
        return self.board_sensor.is_token_on_the_board(distance=distance)

    # Aliases
    sensing_on_board = is_detecting_board  # @deprecated
    is_sensing_on_board = is_detecting_board  # @deprecated

    def on_detecting_borders(self, borders: List[str]):
        """*on_sensing_border* is called, when token is near a border

        Args:
            borders (List): A list of strings with found borders, e.g.: ['left', 'top']

        Examples:

            Register on_sensing_border_event:

            .. code-block::

                @player.register
                def on_sensing_borders(self, borders):
                    print("Player 4: Sensing borders:")
                    print("Borders are here!", str(borders))

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_detecting_borders)

    on_sensing_borders = on_detecting_borders
