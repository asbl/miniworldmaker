import pkgutil
from inspect import isclass

# manually import classes which should be accessible in outer scope.

from miniworldmaker.boards.board_base import BaseBoard
from miniworldmaker.boards.board import Board
from miniworldmaker.boards.pixel_board import PixelBoard
from miniworldmaker.boards.tiled_board import TiledBoard
from miniworldmaker.boards.physics_board import PhysicsBoard
from miniworldmaker.boards.hex_board import HexBoard

from miniworldmaker.tokens.token import Token
from miniworldmaker.tokens.text_token import Text
from miniworldmaker.tokens.number_token import Number
from miniworldmaker.tokens.text_token import TextToken
from miniworldmaker.tokens.number_token import NumberToken

from miniworldmaker.tokens.shapes import Point
from miniworldmaker.tokens.shapes import Line
from miniworldmaker.tokens.shapes import Rectangle
from miniworldmaker.tokens.shapes import Circle
from miniworldmaker.tokens.shapes import Ellipse
from miniworldmaker.tokens.shapes import Polygon
from miniworldmaker.tokens.shapes import Triangle
from miniworldmaker.tokens.shapes import Arc

from miniworldmaker.appearances.appearance import Appearance
from miniworldmaker.appearances.background import Background
from miniworldmaker.appearances.costume import Costume

from miniworldmaker.tools.timer import timer
from miniworldmaker.tools.timer import loop

from miniworldmaker.board_positions.board_vector import Vector
from miniworldmaker.board_positions.board_position import Position

from miniworldmaker.exceptions.miniworldmaker_exception import CostumeOutOfBoundsError

import nest_asyncio
nest_asyncio.apply()

# auto import all classes, so that every class is imported

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)


__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
    for attribute_name in dir(_module):
        attribute = getattr(_module, attribute_name)
        if isclass(attribute):  
            globals()[attribute_name] = attribute
            __all__.append(attribute.__name__)


__all__.append(timer.__name__)
__all__.append(loop.__name__)
