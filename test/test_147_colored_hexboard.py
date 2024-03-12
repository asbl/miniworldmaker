from miniworldmaker import App, Board, Token, Position, HexBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test147(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = HexBoard(24, 2)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.tile_size = 40
                assert board.columns == 24
                assert board.rows == 2
                for x in range(board.columns):
                    for y in range(board.rows):
                        t = Token((x,y))
                        color = (x + y) / (board.columns + board.rows) * 255
                        t.fill_color = (color, color, color)
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



        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()