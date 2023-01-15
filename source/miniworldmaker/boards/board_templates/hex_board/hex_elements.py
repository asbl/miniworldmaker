from abc import ABC
from collections import OrderedDict
from typing import Union

import miniworldmaker.base.app as app
import miniworldmaker.boards.board_templates.tiled_board.tile as tile
import miniworldmaker.boards.board_templates.tiled_board.corner as corner
import miniworldmaker.boards.board_templates.tiled_board.edge as edge
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.positions.position as board_position
from miniworldmaker.boards.board_templates.hex_board import cube_coord


class HexBase(tile_elements.TileBase, ABC):
    @staticmethod
    def get_local_center_coordinate() -> "board_position.BoardPosition":
        """Gets the local center coordinate of each tile.
        """
        board = app.App.running_board
        return board_position.Position("Position", x=board.get_tile_width() / 2, y=board.get_tile_height() / 2)

    def _internal_coordinates(self):
        return cube_coord.CubeCoord

    def _external_coordinates(self):
        return cube_coord.CubeCoord


class HexTile(HexBase, tile.Tile):
    tile_vectors = {
        "w": (+1, 0, -1),
        "nw": (+1, -1, 0),
        "no": (0, -1, +1),
        "o": (-1, 0, +1),
        "so": (-1, +1, 0),
        "sw": (0, +1, -1),
    }

    corner_vectors = OrderedDict(
        [
            ("n", (+1, 0, +1)),
            ("nw", (+1, 0, 0)),
            ("sw", (+1, +1, 0)),
            ("s", (0, +1, 0)),
            ("so", (0, +1, +1)),
            ("no", (0, 0, +1)),
        ]
    )

    edge_vectors = {
        "w": (1, 0.5, 0),
        "no": (1, 0, 0.5),
        "nw": (0, -1, -0.5),
        "o": (0, 0.5, 1),
        "so": (0.5, 1, 0),
        "sw": (0.5, 1, 0.5),
    }

    @staticmethod
    def _get_corner_cls():
        return HexCorner

    @staticmethod
    def _get_edge_cls():
        return HexEdge

    def is_in_tile(self, pixel_position: "board_position.BoardPosition") -> bool:
        """Returns True, if coordinate is in tile.
        :param pixel_position: board position in pixels
        :return: True, if coordinate is in tile
        """
        distance = self.distance(pixel_position, self.to_center())
        for neighbour in self.get_neighbours():
            if distance(pixel_position, neighbour.to_center()) > distance:
                return False
        return True

    def get_corner(self, direction: Union[str, tuple]) -> "CubeCoord":
        """Gets corner by direction
        :param direction: A string (e.g. nw, for north-west corner) or a direction-vector
        :return: The corner.
        """
        if type(direction) == str:
            vector = self.corner_vectors[direction]
        else:
            vector = direction
        return self.board.get_corner(self.position + vector)

    def __str__(self):
        return f"Hex-Tile at {self.position}"

    def _internal_coordinates(self):
        return cube_coord.CubeCoord

    def _external_coordinates(self):
        return cube_coord.CubeCoord

    def __eq__(self, other):
        if self.position == other.position:
            return True
        else:
            return False

    @staticmethod
    def get_position_pixel_dict():
        board = app.App.running_board
        return board.get_center_points()

    def to_pixel(self) -> "board_position.BoardPosition":
        """gets topleft position of tile
        """
        return self.int_coord.to_pixel(
            self.position, (self.board.get_tile_width() / 2, self.board.get_tile_height() / 2), (0, 0)
        )


class HexCorner(HexBase, corner.Corner):
    angles = {"n": 2, "no": 3, "so": 4, "s": 5, "sw": 0, "nw": 1}
    direction_angles = {"n": 0, "no": 0, "so": 0, "s": 0, "sw": 0, "nw": 0}

    tile_vectors = {
        "n": [(-1, -1, 0), (0, -1, -1), (-1, 0, -1)],
        "nw": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
        "sw": [(-1, 0, -1), (0, -1, -1), (-1, -1, 0)],
        "s": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
        "so": [(-1, -1, 0), (-1, 0, -1), (0, -1, -1)],
        "no": [(0, -1, 0), (0, 0, -1), (-1, 0, 0)],
    }

    corner_vectors = {
        "n": [(0, -1, 0), (-1, 0, 0), (0, 0, -1)],
        "nw": [(0, 0, 1), (0, 1, 0), (0, 0, 1)],
        "sw": [(0, -1, 0), (0, -1, 0), (0, 0, -1)],
        "s": [(0, 1, 0), (0, 1, 0), (1, 0, 0)],
        "so": [(0, -1, 0), (-1, 0, 0), (0, 0, -1)],
        "no": [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    }

    def __eq__(self, __o: object) -> bool:
        if type(__o) == HexCorner and self.position == __o.position:
            return True
        else:
            return False

    def __str__(self) -> str:
        corner_str = "Corner at"
        for position in self.positions:
            corner_str += f"({position})"
        return corner_str

    def _internal_coordinates(self):
        return cube_coord.CubeCoord

    def _external_coordinates(self):
        return cube_coord.CubeCoord

    @staticmethod
    def direction_vectors():
        return HexTile.corner_vectors


class HexEdge(HexBase, edge.Edge):
    tile_vectors = {
        "w": [(-1, 0.5, 0), (0, 0.5, -1)],
        "sw": [(-0.5, 1, 0), (-0.5, 0, 1)],
        "so": [(1, 0, 0.5), (0, 1, 0.5)],
        "o": [(-1, -0.5, 0), (0, -0.5, -1)],
        "no": [(-0.5, 1, 0), (-0.5, 0, 1)],
        "nw": [(1, 0, 0.5), (0, 1, 0.5)],
    }

    corner_vectors = {
        "w": [(0, -0.5, 0), (0, 0.5, 0)],
        "sw": [(0.5, 0, 0), (-0.5, 0, 0)],
        "so": [(0, 0, 0.5), (0, 0, -0.5)],
        "o": [(0, -0.5, 0), (0, 0.5, 0)],
        "no": [(0.5, 0, 0), (-0.5, 0, 0)],
        "nw": [(0, 0, 0.5), (0, 0, -0.5)],
    }

    direction_angles = {"o": 0, "so": -60, "sw": 60, "w": 0, "nw": -60, "no": 60}

    angles = {"o": 3, "so": 4, "sw": 5, "w": 0, "nw": 1, "no": 2}

    def __str__(self) -> str:
        edge_str = "Edge at"
        for position in self.positions:
            edge_str += f"({position})"
        return edge_str

    @classmethod
    def from_tile(cls, tile: "board_position.BoardPosition", direction: str, board=None) -> "HexEdge":
        """
        gets a Edge from tile-position and direction
        :param tile: External coordinates for tile
        :param direction: direction as string.
        :return: the HexEdge
        """
        if not board:
            board = app.App.running_board
        return HexEdge(tile, direction, board)

    @staticmethod
    def direction_vectors():
        return HexTile.edge_vectors

    def _internal_coordinates(self):
        return cube_coord.CubeCoord

    def _external_coordinates(self):
        return cube_coord.CubeCoord
