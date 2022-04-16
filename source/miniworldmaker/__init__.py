import pkgutil
from inspect import isclass

import sys
from miniworldmaker import conf

sys.path.append(conf.ROOT_DIR)

# manually import classes which should be accessible in outer scope.

from boards.board_base import BaseBoard
from boards.board import Board
from boards.pixel_board import PixelBoard
from boards.tiled_board import TiledBoard
from boards.physics_board import PhysicsBoard
from boards.hex_board import HexBoard

from tokens.token_base import BaseToken
from tokens.token import Token
from tokens.text_token import Text
from tokens.number_token import Number
from tokens.text_token import TextToken
from tokens.number_token import NumberToken

from tokens.shapes import Point
from tokens.shapes import Line
from tokens.shapes import Rectangle
from tokens.shapes import Circle
from tokens.shapes import Ellipse
from tokens.shapes import Polygon
from tokens.shapes import Triangle
from tokens.shapes import Arc

from appearances import appearance_base
from appearances.appearance import Appearance
from appearances.appearance_base import AppearanceBase
from appearances.background import Background
from appearances.costume import Costume

from tools.timer import timer
from tools.timer import loop

from board_positions.board_vector import Vector
from board_positions.board_position import Position

from exceptions.miniworldmaker_exception import CostumeOutOfBoundsError



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
