from tools import appearance


class Background(appearance.Appearance):
    def __init__(self, board):
        self.board = board
        super().__init__()
        self.size = (self.board.width, self.board.height)
