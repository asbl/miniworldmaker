import miniworldmaker.boards.board_templates.hex_board.hex_elements as hex_elements
import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements


class TileFactory:
    def __init__(self):
        self.tile_cls = tile_elements.Tile
        self.corner_cls = tile_elements.Corner
        self.edge_cls = tile_elements.Edge


class HexTileFactory:
    def __init__(self):
        self.tile_cls = hex_elements.HexTile
        self.corner_cls = hex_elements.HexCorner
        self.edge_cls = hex_elements.HexEdge
