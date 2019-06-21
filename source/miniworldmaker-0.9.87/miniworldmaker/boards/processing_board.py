from miniworldmaker.boards.pixel_board import PixelBoard


class ProcessingBoard(PixelBoard):

    def __init__(self, columns=400, rows=300, color=(0,0,0,0)):
        super().__init__(columns=columns, rows=rows)
        self.background.set_fill_color(color)

