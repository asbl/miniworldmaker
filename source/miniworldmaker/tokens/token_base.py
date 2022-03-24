from __future__ import annotations
from miniworldmaker.exceptions.miniworldmaker_exception import (
    NoValidBoardPositionError,
    TokenArgumentShouldBeTuple,
    NotImplementedOrRegisteredError,
    NoBoardError,
)
from typing import Tuple, Union, Type, TypeVar, List, Optional, Tuple
from miniworldmaker.appearances import appearance
from miniworldmaker.appearances import costume
from miniworldmaker.appearances import costumes_manager
from miniworldmaker.board_positions import board_position
from miniworldmaker.exceptions.miniworldmaker_exception import (
    NotImplementedOrRegisteredError,
    NoBoardError,
)
from miniworldmaker.tools import token_inspection
from miniworldmaker.dialogs import ask
import miniworldmaker
import pygame

class Meta(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = type.__call__(cls, *args, **kwargs) # create a new Token
        except NoValidBoardPositionError:
            raise TokenArgumentShouldBeTuple()
        # Add token to board **after** init
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board(instance._position)
        return instance

class BaseToken(pygame.sprite.DirtySprite, metaclass=Meta):
    token_count: int = 0
    class_image: str = ""

    def __init__(self, position: Optional[Union[Tuple, "miniworldmaker.BoardPosition"]] = None):
        self._collision_type: str = ""
        self._layer: int = 0
        self._inner = 0
        self._managers: list = list()
        self.token_id: int = BaseToken.token_count + 1
        self.costume_manager: costumes_manager.CostumesManager = None
        self.board_sensor: miniworldmaker.TokenBoardSensor = None
        self.position_manager: miniworldmaker.TokenPositionManager = None
        self.board: miniworldmaker.Board = miniworldmaker.App.board
        if not self.board:
            raise NoBoardError()
        _token_connector = self.board.get_token_connector(self)
        _token_connector.add_token_managers(position)  
        pygame.sprite.DirtySprite.__init__(self)
        BaseToken.token_count += 1
        self.static: bool = False
        self.speed: int = 1
        self._position: "board_position.BoardPosition" = position
        self.ask: "ask.Ask" = ask.Ask(self.board)

    def __str__(self):
        if self.board and hasattr(self.board, "position_manager"):
            return "{0}-Object, ID: {1} at pos {2} with size {3}".format(
                self.class_name, self.token_id, self.position, self.size
            )
        else:
            return "**: {0}; ID: {1}".format(self.class_name, self.token_id)

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
        if self.costume_manager:
            return self.costume_manager.dirty

    @dirty.setter
    def dirty(self, value: int):
        if self.costume_manager:
            self.costume_manager.dirty = value

    @property
    def rect(self) -> pygame.Rect:
        """
        The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.
        """
        return self.position_manager.rect

    def get_rect(self) -> pygame.Rect:
        return self.position_manager.rect