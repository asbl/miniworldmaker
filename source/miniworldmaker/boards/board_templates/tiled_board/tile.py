from __future__ import annotations

from collections import OrderedDict
from typing import List, Optional
from typing import TYPE_CHECKING
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.base.app as app
import miniworldmaker.positions.position as board_position

if TYPE_CHECKING:
    import miniworldmaker.boards.board_templates.tiled_board.corner as corner
    import miniworldmaker.boards.board_templates.tiled_board.tiled_board as tiled_board_mod
    import miniworldmaker.positions.vector as board_vector



class Tile(tile_elements.TileBase):
    tile_vectors = {
        "w": (+1, 0),
        "nw": (+1, +1),
        "no": (-1, +1),
        "o": (-1, 0),
        "so": (-1, -1),
        "sw": (+1, -1),
    }

    corner_vectors = OrderedDict(
        [
            ("nw", (+0.5, +0.5)),
            ("no", (-0.5, +0.5)),
            ("so", (-0.5, -0.5)),
            ("sw", (+0.5, -0.5)),
        ]
    )

    edge_vectors = {
        "w": (-0.5, 0),
        "o": (+0.5, 0),
        "s": (0, +0.5),
        "n": (0, -0.5),
    }

    @classmethod
    def from_position(cls, position, board: "tiled_board_mod.TiledBoard" = None) -> "tile_elements.TileBase":
        return board.get_tile(position)

    @classmethod
    def from_token(cls, token):
        return token.board.get_tile(token.position)

    def __init__(self, position, board=None):
        super().__init__(position, board)
        self.tiles = []
        self.corners = []
        self.edges = []

    def get_neighbour_corners(self) -> List["corner.Corner"]:
        if self.corners:
            return self.corners
        else:
            neighbours = []
            for corner, vector in self.corner_vectors.items():
                neighbour = self.board.get_corner(self.position + vector)
                if neighbour:
                    neighbours.append(neighbour)
            self.corners = neighbours
            return self.corners

    def to_pixel(self) -> "board_position.Position":
        x = self.position[0] * self.board.tile_size
        y = self.position[1] * self.board.tile_size
        return board_position.Position(x, y)

    @staticmethod
    def get_position_pixel_dict(board):
        return board.get_center_points()

    def to_center(self):
        topleft = self.to_pixel()
        return topleft + self.get_local_center_coordinate(self.board)

    @classmethod
    def from_pixel(cls, pixel_position,
                   board: Optional["tiled_board_mod.TiledBoard"] = None) -> "tile_elements.TileBase":
        if not board:
            board = app.App.running_board
        x = pixel_position[0] // board.tile_size
        y = pixel_position[1] // board.tile_size
        return cls((x, y), board=None)

    def __sub__(self, other):
        import miniworldmaker.positions.vector as board_vector #t
        return board_vector.Vector(self.position[0] - other.position[0], self.position[1] - other.position[1])

    def distance_to(self, other):
        vec = self - other
        return vec.length()
