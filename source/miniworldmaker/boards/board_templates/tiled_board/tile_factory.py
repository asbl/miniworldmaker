import miniworldmaker.boards.board_templates.hex_board.hex_elements as hex_elements
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.boards.board_templates.tiled_board.tile as tile_mod
import miniworldmaker.boards.board_templates.tiled_board.corner as corner_mod
import miniworldmaker.boards.board_templates.tiled_board.edge as edge_mod


class TileFactory:
    def __init__(self):
        self.tile_cls = tile_mod.Tile
        self.corner_cls = corner_mod.Corner
        self.edge_cls = edge_mod.Edge


class HexTileFactory:
    def __init__(self):
        self.tile_cls = hex_elements.HexTile
        self.corner_cls = hex_elements.HexCorner
        self.edge_cls = hex_elements.HexEdge
