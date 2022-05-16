from __future__ import annotations

from typing import Union, Optional, Tuple

import pygame
import functools

import miniworldmaker.appearances.costumes_manager as costumes_manager
import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.boards.board as board
import miniworldmaker.dialogs.ask as ask
import miniworldmaker.tokens.positions.token_position_manager as token_position_manager
import miniworldmaker.tools.token_inspection as token_inspection
import miniworldmaker.tokens.sensors.token_boardsensor as token_boardsensor
from miniworldmaker.exceptions.miniworldmaker_exception import (
    NoValidBoardPositionError,
    TokenArgumentShouldBeTuple,
    NoBoardError,
)


class Meta(type):
    def __call__(cls, *args, **kwargs):
        if len(args) >= 2 and type(args[0]) == int and type(args[1]) == int:
            first = (args[0], args[1])
            last_args = [args[n] for n in range(2, len(args))]
            args = [first] + last_args
        instance = type.__call__(cls, *args, **kwargs)  # create a new Token
        # Add token to board **after** init
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board(instance._position)
        return instance


class BaseToken(pygame.sprite.DirtySprite, metaclass=Meta):
    token_count: int = 0
    class_image: str = ""

    def __init__(self, position: Optional[Union[Tuple, "board_position.Position"]] = None):
        self._collision_type: str = "rect"
        self._layer: int = 0
        self._inner = 0
        self._dirty = 1
        self._size = (0, 0)
        self._static = False
        self._position: "board_position.Position" = position
        self._managers: list = list()
        self.token_id: int = BaseToken.token_count + 1
        self.costume_manager: costumes_manager.CostumesManager = None
        self.board_sensor: token_boardsensor.TokenBoardSensor = None
        self.position_manager: token_position_manager.TokenPositionManager = None
        self.board: "board.Board" = app.App.board
        if not self.board:
            raise NoBoardError()
        _token_connector = self.board.get_token_connector(self)
        _token_connector.add_token_managers(position)
        # properties defined in subclasses
        # end
        pygame.sprite.DirtySprite.__init__(self)
        BaseToken.token_count += 1
        self.speed: int = 1
        self.ask: "ask.Ask" = ask.Ask(self.board)

    @property
    def position(self) -> "board_position.BoardPosition":
        """implemented in subclass"""
        return board_position.Position(0, 0)

    @property
    def size(self) -> Tuple:
        """implemented in subclass"""
        return self._size

    @property
    def static(self) -> bool:
        """implemented in subclass"""
        return self._static

    def __str__(self):
        if self.board and hasattr(self.board, "position_manager"):
            return "{0}-Object, ID: {1} at pos {2} with size {3}".format(
                self.__class__.__name__, self.token_id, self.position, self.size
            )
        else:
            return "**: {0}; ID: {1}".format(self.__class__.__name__, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        """
        The image of the token:

        .. warning::
          Warning: You should not directly draw on the image
          as the image will be reloaded during animations

        """
        return self.costume_manager.image

    @property
    def dirty(self) -> int:
        """If token is dirty, it will be repainted.

        Returns:

            int: 1 if token is dirty/0 otherwise
        """
        return self._dirty

    @dirty.setter
    def dirty(self, value: int):
        self._dirty = value

    @property
    def rect(self) -> pygame.Rect:
        """
        The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.
        """
        return self.position_manager.rect

    def get_rect(self) -> pygame.Rect:
        return self.position_manager.rect

    def register(self, method: callable):
        """This method is used for the @register decorator. It adds a method to an object

        Args:
            method (callable): The method which should be added to the token
        """
        bound_method = token_inspection.TokenInspection(self).bind_method(method)
        if method.__name__ == "on_setup":
            self.on_setup()
        self.board.event_manager.register_event(method.__name__, self)
        return bound_method
