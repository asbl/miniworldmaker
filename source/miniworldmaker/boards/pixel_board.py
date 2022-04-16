from typing import Union

import pygame

import sys
from miniworldmaker import conf

sys.path.append(conf.ROOT_DIR)

from board_positions import board_position
from boards import board as board_module
from boards.token_connectors.pixel_board_connector import PixelBoardConnector
from tokens import token as token_module
import miniworldmaker


class PixelBoard(miniworldmaker.Board):
    pass