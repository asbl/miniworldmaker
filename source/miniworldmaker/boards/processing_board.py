from miniworldmaker.boards import pixel_board as pb


class ProcessingBoard(pb.PixelBoard):
    """
    A ProcessingBoard

    Args:
        width: The width of the board in Pixels (default: 400)
        height: The height of the board in pixels (default: 300)
    """

    def __init__(self, width=400, height=300):
        super().__init__(columns=width, rows=height)





