import inspect
import os
import sys

import pygame

pygame.init()

# __import__('pkg_resources').declare_namespace(__name__)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

__all__ = []

from miniworldmaker.base.app import App

from miniworldmaker.boards.board_templates.pixel_board.board import Board
from miniworldmaker.boards.board_templates.pixel_board.pixel_board import PixelBoard
from miniworldmaker.boards.board_templates.tiled_board.tiled_board import TiledBoard
from miniworldmaker.boards.board_templates.physics_board.physics_board import PhysicsBoard as PhysicsBoard
from miniworldmaker.boards.board_templates.hex_board.hex_board import HexBoard
from miniworldmaker.boards.board_templates.toolbar.toolbar import Toolbar
from miniworldmaker.boards.board_templates.console.console import Console

from miniworldmaker.tokens.token_base import BaseToken
from miniworldmaker.tokens.token import Token
from miniworldmaker.tokens.actor import Actor
from miniworldmaker.tokens.token_plugins.text_token.text_token import Text
from miniworldmaker.tokens.token_plugins.text_token.number_token import Number
from miniworldmaker.tokens.token_plugins.text_token.text_token import TextToken
from miniworldmaker.tokens.token_plugins.text_token.number_token import NumberToken
from miniworldmaker.tokens.token_plugins.sensors.sensor import Sensor
from miniworldmaker.tokens.token_plugins.sensors.circle_sensor import CircleSensor

from miniworldmaker.tokens.token_plugins.shapes.shapes import Point
from miniworldmaker.tokens.token_plugins.shapes.shapes import Rectangle
from miniworldmaker.tokens.token_plugins.shapes.shapes import Circle
from miniworldmaker.tokens.token_plugins.shapes.shapes import Line
from miniworldmaker.tokens.token_plugins.shapes.shapes import Ellipse
from miniworldmaker.tokens.token_plugins.shapes.shapes import Polygon
from miniworldmaker.tokens.token_plugins.shapes.shapes import Triangle
from miniworldmaker.tokens.token_plugins.shapes.shapes import Arc

from miniworldmaker.appearances.appearance import Appearance
from miniworldmaker.appearances.background import Background
from miniworldmaker.appearances.costume import Costume

from miniworldmaker.tools.timer import timer
from miniworldmaker.tools.timer import loop
from miniworldmaker.tools.timer import ActionTimer
from miniworldmaker.tools.timer import LoopActionTimer
from miniworldmaker.tools.timer import Timer



"""
from miniworldmaker.containers.widgets import Widget
from miniworldmaker.containers.widgets import Button
from miniworldmaker.containers.widgets import Label
from miniworldmaker.containers.widgets import ToolbarLabel
from miniworldmaker.containers.widgets import ToolbarButton
from miniworldmaker.containers.widgets import YesNoButton
from miniworldmaker.containers.widgets import CounterLabel
from miniworldmaker.containers.widgets import SimplePagination
"""

from miniworldmaker.tokens.token_plugins.widgets.button import Button
from miniworldmaker.tokens.token_plugins.widgets.button import ToolbarButton
from miniworldmaker.tokens.token_plugins.widgets.label import Label
from miniworldmaker.tokens.token_plugins.widgets.label import ToolbarLabel
from miniworldmaker.tokens.token_plugins.widgets.yesno import YesNoButton


from miniworldmaker.containers.actionbar import ActionBar
"""
from miniworldmaker.containers.console import Console
from miniworldmaker.containers.event_console import EventConsole
from miniworldmaker.containers.inspect_actor_toolbar import InspectActorToolbar
from miniworldmaker.containers.level_designer_toolbar import LevelDesignerToolbar
from miniworldmaker.containers.color_toolbar import ColorToolbar
"""

from miniworldmaker.positions.vector import Vector
from miniworldmaker.positions.position import Position
from miniworldmaker.positions.direction import Direction
from miniworldmaker.positions.rect import Rect

from miniworldmaker.boards.board_templates.tiled_board.tile_factory import TileFactory
from miniworldmaker.boards.board_templates.tiled_board.tile_factory import HexTileFactory

from miniworldmaker.boards.board_templates.hex_board.hex_elements import HexBase
from miniworldmaker.boards.board_templates.hex_board.hex_elements import HexEdge
from miniworldmaker.boards.board_templates.hex_board.hex_elements import HexTile
from miniworldmaker.boards.board_templates.hex_board.hex_elements import HexCorner

from miniworldmaker.boards.board_templates.hex_board.cube_coord import CubeCoord

from miniworldmaker.boards.board_templates.tiled_board.tile_elements import TileBase
from miniworldmaker.boards.board_templates.tiled_board.edge import Edge
from miniworldmaker.boards.board_templates.tiled_board.tile import Tile
from miniworldmaker.boards.board_templates.tiled_board.corner import Corner

from miniworldmaker.exceptions.miniworldmaker_exception import CostumeOutOfBoundsError

__all__.append(App.__name__)
__all__.append(Board.__name__)
__all__.append(PixelBoard.__name__)
__all__.append(PhysicsBoard.__name__)
__all__.append(TiledBoard.__name__)
__all__.append(HexBoard.__name__)
__all__.append(BaseToken.__name__)
__all__.append(Token.__name__)
__all__.append(Actor.__name__)
__all__.append(Text.__name__)
__all__.append(Number.__name__)
__all__.append(TextToken.__name__)
__all__.append(NumberToken.__name__)

__all__.append(Point.__name__)
__all__.append(Rectangle.__name__)
__all__.append(Line.__name__)
__all__.append(Ellipse.__name__)
__all__.append(Polygon.__name__)
__all__.append(Triangle.__name__)
__all__.append(Arc.__name__)
__all__.append(Circle.__name__)

__all__.append(Sensor.__name__)
__all__.append(CircleSensor.__name__)

__all__.append(Appearance.__name__)
__all__.append(Background.__name__)
__all__.append(Costume.__name__)

__all__.append(Vector.__name__)
__all__.append(Position.__name__)
__all__.append(Rect.__name__)
__all__.append(Direction.__name__)

__all__.append(Toolbar.__name__)
__all__.append(ActionBar.__name__)

__all__.append(Console.__name__)
"""
__all__.append(EventConsole.__name__)
__all__.append(InspectActorToolbar.__name__)
__all__.append(LevelDesignerToolbar.__name__)
__all__.append(ColorToolbar.__name__)
"""
__all__.append(ToolbarLabel.__name__)
__all__.append(ToolbarButton.__name__)
__all__.append(YesNoButton.__name__)
"""
__all__.append(CounterLabel.__name__)

__all__.append(SimplePagination.__name__)"""
__all__.append(Label.__name__)
__all__.append(Button.__name__)

__all__.append(TileFactory.__name__)
__all__.append(HexTileFactory.__name__)

__all__.append(HexBase.__name__)
__all__.append(HexEdge.__name__)
__all__.append(HexTile.__name__)
__all__.append(HexCorner.__name__)
__all__.append(CubeCoord.__name__)

__all__.append(TileBase.__name__)
__all__.append(Corner.__name__)
__all__.append(Tile.__name__)
__all__.append(Edge.__name__)

__all__.append(timer.__name__)
__all__.append(loop.__name__)

__all__.append(ActionTimer.__name__)
__all__.append(LoopActionTimer.__name__)
__all__.append(Timer.__name__)

__all__.append(CostumeOutOfBoundsError.__name__)
