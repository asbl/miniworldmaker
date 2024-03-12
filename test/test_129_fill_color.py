from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test129(unittest.TestCase):

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
        board = PixelBoard()
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            token = Token()
            token.fill_color = (0, 0, 255)
            token.size = (20,80)

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

