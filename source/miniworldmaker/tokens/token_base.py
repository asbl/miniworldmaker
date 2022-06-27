from __future__ import annotations
from shelve import Shelf

from typing import Union, Optional, Tuple
from numpy import isin

import pygame
import functools
import collections

import miniworldmaker.base.app as app

from miniworldmaker.exceptions.miniworldmaker_exception import (
    MiniworldMakerError,
    NoValidBoardPositionError,
    TokenArgumentShouldBeTuple,
    WrongArgumentsError,
)


class Meta(type):
    def __call__(cls, *args, **kwargs):
        if len(args) >= 2 and type(args[0]) == int and type(args[1]) == int:
            first = (args[0], args[1])
            last_args = [args[n] for n in range(2, len(args))]
            args = [first] + last_args
        instance = type.__call__(cls, *args, **kwargs)  # create a new Token
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board(instance._position)
        return instance


class BaseToken(pygame.sprite.DirtySprite, metaclass=Meta):

    def __init__(self):
        self.board: "board.Board" = app.App.board
        self._managers: list = list()

    def _get_new_costume(self):
        return self.board.get_token_connector(self).create_costume()
        
    def _init_board_sensor(self):
        self._board_sensor = self.board.get_token_connector(self).create_board_sensor()
        self._managers.append(self._board_sensor)
        return self._board_sensor

    def _init_costume_manager(self):
        self._costume_manager = self.board.get_token_connector(self).create_costume_manager()
        self._costume_manager._add_default_appearance()
        self._managers.append(self._costume_manager)
        return self._costume_manager

    def _init_position_manager(self):
        self._position_manager = self.board.get_token_connector(self).create_position_manager()
        self._position_manager.position = self._position
        self._managers.append(self._position_manager)
        return self._position_manager

    @property
    def dirty(self) -> int:
        """If token is dirty, it will be repainted.

        Returns:

            int: 1 if token is dirty/0 otherwise
        """
        return self._dirty
    
    @dirty.setter
    def dirty(self, value: int):
        if not self._dirty and self.position_manager and self.board.camera.is_token_in_viewport(self) and value == 1:
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