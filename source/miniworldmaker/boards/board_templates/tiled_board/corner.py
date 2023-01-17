import math
from typing import Optional

import miniworldmaker.base.app as app
import miniworldmaker.boards.board_templates.tiled_board.tile as tile
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.boards.board_templates.tiled_board.tiled_board as tiled_board_mod


class Corner(tile_elements.TileDelimiter):
    angles = {
        "no": 0,
        "nw": 1,
        "sw": 2,
        "so": 3,
    }

    direction_angles = {
        "no": 0,
        "nw": 0,
        "sw": 0,
        "so": 0,
    }

    @staticmethod
    def direction_vectors():
        return tile.Tile.corner_vectors

    @classmethod
    def from_position(cls, position, board: "tiled_board_mod.TiledBoard"):
        return board.get_corner(position)

    @classmethod
    def from_pixel(cls, position, board: Optional["tiled_board_mod.TiledBoard"] = None):
        if not board:
            board = app.App.window.container_manager.get_container_by_pixel(position[0], position[1])
        min_value = math.inf
        nearest_hex = None
        corner_points = board.get_corner_points()
        for corner_position, corner_pos in corner_points.items():
            distance = math.sqrt(pow(position[0] - corner_pos[0], 2) + pow(position[1] - corner_pos[1], 2))
            if distance < min_value:
                min_value = distance
                nearest_hex = corner_position
        return cls.from_position(nearest_hex, board)

    @classmethod
    def from_tile(cls, position, direction_string):
        board = app.App.running_board
        tile = board.get_tile(position)
        return board.get_corner(tile.position + cls.get_direction_from_string(direction_string))

    def start_angle(self):
        return 0.5
