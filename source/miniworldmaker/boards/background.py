from tools import appearance


class Background(appearance.Appearance):
    def __init__(self, board):
        self.board = board
        super().__init__()
        self.size = (self.board.width, self.board.height)

    def next_sprite(self):
        super().next_sprite()
        self.board.window.repaint_areas.append(self.image.get_rect())
        self.board.window.window_surface.blit(self.image, (0, 0))
