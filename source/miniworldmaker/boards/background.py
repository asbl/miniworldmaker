from tools import appearance


class Background(appearance.Appearance):
    def __init__(self, board):
        self.board = board
        super().__init__()
        self._renderer.set_image_action("info_overlay", False)
        self._renderer.set_image_action("scale_x", True)
        self._renderer.set_image_action("scale_y", True)
        self._renderer.set_image_action("upscale", False)

    @property
    def image(self):
        self._renderer.size = (self.board.width, self.board.height)
        self._renderer.tiles = (self.board.columns, self.board.rows)
        self._renderer.tile_size = self.board.tile_size
        self._renderer.margin = self.board.tile_margin
        self._image = self._renderer.get_image()
        return self._image
