import miniworldmaker.boards.board_templates.tiled_board.tile as tile
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.boards.board_templates.tiled_board.tiled_board as tiled_board_mod


class Edge(tile_elements.TileDelimiter):
    tile_vectors = {
        "w": [(-0.5, 0), (0.5, 0)],
        "n": [(0, 0.5), (0, -0.5)],
        "o": [(-0.5, 0), (0.5, 0)],
        "s": [(0, 0.5), (0, -0.5)],
    }

    direction_angles = {
        "o": 0,
        "s": 90,
        "w": 0,
        "n": 90,
    }

    angles = {
        "o": 0,
        "s": 1,
        "w": 2,
        "n": 3,
    }

    @staticmethod
    def direction_vectors():
        return tile.Tile.edge_vectors

    @staticmethod
    def get_position_pixel_dict(board):
        return board.get_edge_points()

    @classmethod
    def from_position(cls, position, board: "tiled_board_mod.TiledBoard"):
        return board.get_edge(position)

    def start_angle(self):
        return 0
