from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test133(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        board = Board(210,80)
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            board.default_border_color = (0,0, 255)
            board.default_border = 1

            t = Token((10,10))

            t2 = Token ((60, 10))
            t2.border_color = (0,255, 0)
            t2.border = 5 # overwrites default border

            t3 = Token ((110, 10))
            t3.border = None # removes border

            t4 = Token ((160, 10))
            t4.add_costume("images/player.png") # border for sprite

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()