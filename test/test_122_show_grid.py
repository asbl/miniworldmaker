from miniworldmaker import App, Board, TiledBoard, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test122(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard(4,4)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.tile_margin = 10
                background = board.add_background("images/stone.png")
                background.is_textured = True
                token = Token()
                background.grid = True
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()