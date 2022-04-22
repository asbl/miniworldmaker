import miniworldmaker.board_positions.tile_elements as tile_elements
import miniworldmaker.board_positions.hex_elements as hex_elements


class TileFactory():
    def __init__(self):
        self.tile_cls = tile_elements.Tile
        self.corner_cls = tile_elements.Corner
        self.edge_cls = tile_elements.Edge


class HexTileFactory():
    def __init__(self):
        self.tile_cls = hex_elements.HexTile
        self.corner_cls = hex_elements.HexCorner
        self.edge_cls = hex_elements.HexEdge
