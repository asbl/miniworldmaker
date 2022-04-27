import math
from typing import Union, Tuple, Dict

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.hex_elements as hex_elements
import miniworldmaker.board_positions.tile_factory as tile_factory
import miniworldmaker.boards.tiled_board as tiled_board
import miniworldmaker.boards.token_connectors.hex_board_connector as hex_board_connector
from miniworldmaker.exceptions import miniworldmaker_exception


class HexBoard(tiled_board.TiledBoard):
    """
    A hexboard is a board that consists of hexagonal tiles.

    Each token can be positioned either at a tile, at an edge or at a corner.

    
    """
    def __init__(self, columns: int = 20, rows: int = 16, empty=False):
        super().__init__(columns, rows, empty)
        self.lookup_table = []

    def _get_tile_factory(self):
        return tile_factory.HexTileFactory()

    def _templates(self):
        return hex_elements.HexTile, hex_elements.HexEdge, hex_elements.HexCorner

    def get_type(self, position):
        if self.is_tile(position):
            return hex_elements.HexTile
        elif self.is_corner(position):
            return hex_elements.HexCorner
        elif self.is_edge(position):
            return hex_elements.HexEdge

    def is_tile(self, position):
        position = hex_elements.CubeCoord.create(position)
        if (position[0], position[1], position[2]) in self.tiles:
            return True
        else:
            return False

    def get_tile(self, position):
        position = hex_elements.CubeCoord.create(position)
        if self.is_tile(position):
            return self.tiles[position]
        else:
            raise miniworldmaker_exception.TileNotFoundError(position)

    def is_corner(self, position, direction=None):
        corner_cls = self.tile_factory.corner_cls
        if direction is not None:
            position = corner_cls(position, direction).position
        position = hex_elements.CubeCoord.create(position)
        if (position[0], position[1], position[2]) in self.corners:
            return True
        else:
            return False

    def get_corner(self, position, direction=None):
        corner_cls = self.tile_factory.corner_cls
        if direction is not None:
            position = corner_cls(position, direction).position
        position = hex_elements.CubeCoord.create(position)
        if position in self.corners:
            return self.corners[(position[0], position[1], position[2])]
        else:
            raise miniworldmaker_exception.CornerNotFoundError(position)

    def is_edge(self, position, direction=None):
        edge_cls = self.tile_factory.edge_cls
        if direction is not None:
            position = edge_cls(position, direction).position
        position = hex_elements.CubeCoord.create(position)
        if (position[0], position[1], position[2]) in self.edges:
            return True
        else:
            return False

    def get_edge(self, position, direction=None):
        edge_cls = self.tile_factory.edge_cls
        if direction is not None:
            position = edge_cls(position, direction).position
        position = hex_elements.CubeCoord.create(position)
        if self.is_edge(position):
            return self.edges[(position[0], position[1], position[2])]
        else:
            raise miniworldmaker_exception.EdgeNotFoundError(position)

    def get_tile_from_pixel(self, position):
        return hex_elements.HexTile.from_pixel(position)

    def get_corner_from_tile(self, position: Union["board_position.Position", "hex_elements.CubeCoord"],
                             direction: str):
        position = hex_elements.CubeCoord.create(position)
        return self.tiles[position].get_corner(direction)

    def get_edge_from_tile(self, position: Union["board_position.Position", "hex_elements.CubeCoord"], direction: str):
        position = hex_elements.CubeCoord.create(position)
        return self.tiles[position].get_edge(direction)

    def _hex_to_pixel(self, hex_position, origin):
        return hex_elements.CubeCoord.create(hex_position).to_pixel(size=self.get_hex_size(), origin=origin)

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
        for position, tile in self.tiles.items():
            center = tile.to_center()
            center_points[position] = center
        return center_points

    def get_corner_points(self) -> Dict[Tuple, "board_position.Position"]:
        corner_points = dict()
        for position, corner in self.corners.items():
            corner_points[position] = corner.to_pixel()
        return corner_points

    def get_edge_points(self) -> Dict[Tuple, "board_position.Position"]:
        edge_points = dict()
        for position, edge in self.edges.items():
            edge_points[position] = edge.to_pixel()
        return edge_points

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

    @staticmethod
    def _get_token_connector_class():
        return hex_board_connector.HexBoardConnector

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
