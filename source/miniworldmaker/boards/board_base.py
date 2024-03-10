from abc import ABC
from typing import List

import miniworldmaker.boards.data.export_factory as export_factory
import miniworldmaker.boards.data.import_factory as import_factory
import miniworldmaker.containers.container as container_mod
import pygame
from miniworldmaker.base import app as app_mod
from miniworldmaker.boards.board_manager import board_camera_manager
from miniworldmaker.boards.board_templates.pixel_board import pixel_board_connector as pixel_board_connector
from miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.tokens import token as token_module


class BaseBoard(container_mod.Container, ABC):
    subclasses = None

    def __init__(self):
        super().__init__()
        self.is_tiled = False
        self._is_acting = True

    @staticmethod
    def _get_camera_manager_class():
        return board_camera_manager.BoardCameraManager

    @staticmethod
    def _get_token_connector_class():
        """needed by get_token_connector in parent class"""
        return pixel_board_connector.PixelBoardConnector

    def get_token_connector(self, token) -> token_connector.TokenConnector:
        return self._get_token_connector_class()(self, token)

    def add_container(self, container: "container_mod.Container", dock: str, size=None):
        if isinstance(container, BaseBoard):
            if dock == "right":
                new_board = container
                new_board.rows = new_board.get_rows_by_height(self.container_height)
                if size is not None:
                    new_board.columns = size
                else:
                    size = new_board.width
            if dock == "bottom":
                new_board = container
                new_board.columns = new_board.get_columns_by_width(self.container_width)
                if size is not None:
                    new_board.rows = size
                else:
                    size = new_board.height
            new_board.viewport_height = new_board.height
            new_board.viewport_width = new_board.width
        if self == self.app.running_board:
            _container = self.app.container_manager.add_container(container, dock, size)
            if isinstance(container, BaseBoard):
                app_mod.App.running_boards.append(new_board)
                container.on_change()
            return _container

    def add_board(self, position, board, width=None):
        board = self.add_container(board, position, width)
        return board

    def remove_container(self, container: "container_mod.Container"):
        return self.app.container_manager.remove_container(container)

    @property
    def surface(self):
        return self.background.surface

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def window(self) -> "app_mod.App":
        """
        Gets the parent window

        Returns:
            The window

        """
        return self._window

    def load_board_from_db(self, file: str):
        """
        Loads a sqlite db file.
        """
        return import_factory.ImportBoardFromDB(file, self.__class__).load()

    def load_tokens_from_db(self, file: str, token_classes: list) -> List["token_module.Token"]:
        """Loads all tokens from db. Usually you load the tokens in __init__() or in on_setup()

        Args:
            file (str): reference to db file
            token_classes (list): a list of all Token Classes which should be imported.

        Returns:
            [type]: All Tokens
        """
        return import_factory.ImportTokensFromDB(file, token_classes).load()

    def save_to_db(self, file):
        """
        Saves the current board an all actors to database.
        The file is stored as db file and can be opened with sqlite.

        Args:
            file: The file as relative location

        Returns:

        """
        export = export_factory.ExportBoardToDBFactory(file, self)
        export.remove_file()
        export.save()
        export_factory.ExportTokensToDBFactory(file, self.tokens).save()

    def screenshot(self, filename: str = "screenshot.jpg"):
        """Creates a screenshot in given file.

        Args:
            filename: The location of the file. The folder must exist. Defaults to "screenshot.jpg".
        """
        pygame.image.save(self.app.window.surface, filename)

    def get_background(self):
        """Implemented in subclass"""
        pass

    def get_columns_by_width(self, width):
        return width

    def get_rows_by_height(self, height):
        return height
