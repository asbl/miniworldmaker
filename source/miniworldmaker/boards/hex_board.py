from typing import Union, Tuple, Dict
from collections import defaultdict
from miniworldmaker.boards import tiled_board
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards.token_connectors import hex_board_connector
from miniworldmaker.boards.elements import hex_elements
from miniworldmaker.app import app
import collections
import math

import numpy as np



# Template: https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py

class HexBoard(tiled_board.TiledBoard):
    def __init__(self, columns: int = 20, rows: int = 16):
        super().__init__(columns, rows)
        self.lookup_table = []

    def _templates(self):
        return hex_elements.HexTile, hex_elements.HexEdge, hex_elements.HexCorner

    def get_tile(self, position):
        if type(position) != hex_elements.CubeCoord:
            position = hex_elements.CubeCoord.from_position(position)
        return self.tiles[(position[0], position[1], position[2])]

    def get_tile_from_pixel(self, position):
        return hex_elements.HexTile.from_pixel(position)

    def get_corner(self, position):
        if type(position) != hex_elements.CubeCoord:
            position = hex_elements.CubeCoord.from_position(position)
        return self.corners[position]

    def get_corner_from_tile(self, position, direction):
        if type(position) != hex_elements.CubeCoord:
            position = hex_elements.CubeCoord.from_position(position)
        return self.tiles[position].get_corner(direction)

    def _hex_to_pixel(self, hex_position, origin):
        return hex_elements.OffsetPosition(hex_position[0], hex_position[1]).to_pixel(size=self.get_hex_size(), origin=origin)

    def get_tile_width(self):
        return math.sqrt(3) * (self.base_size() / 2)

    def get_tile_height(self):
        return self.base_size()

    def base_size(self):
        return self.tile_size

    def get_hex_size(self):
        return (self.get_tile_width() / 2, self.get_tile_height() / 2)

    def get_center_points(self) -> Dict[Tuple, "board_position.Position"]:
        center_points = dict() 
        for x in range(self.columns):
            for y in range(self.rows):
                center_points[x, y] = self.get_tile((x, y)).to_center()
        return center_points

    def get_from_pixel(self, pixel):
        return hex_elements.HexTile.from_pixel(pixel)

    def to_pixel(self, position):
        return self._hex_to_pixel(position, (0, 0))

    def to_edge(self, position, corner):
        pixel = self.layout.hex_to_pixel(position)
        offset = self.layout.hex_corner_offset(corner)
        corner = pixel + offset
        return corner

    def get_corner_position(self, position, corner):
        return self.get_corner_from_tile(position, corner).get_position()

    def draw_on_image(self, image, position):
        position = self.to_pixel(position)
        self.background.draw_on_image(image, position, self.get_tile_width(), self.get_tile_height())

    def get_token_connector(self, token) -> "hex_board_connector.HexBoardConnector":
        return hex_board_connector.HexBoardConnector(self, token)

    def set_tile_size(self, value):
        super().set_tile_size(value)

    @property
    def container_width(self) -> int:
        """The width of the container"""
        return self.columns * self.get_tile_width() + 1 / 2 * self.get_tile_width()

    @property
    def container_height(self) -> int:
        """The height of the container"""
        return self.rows * self.get_tile_height() * 3 / 4 + self.get_tile_height() / 4
