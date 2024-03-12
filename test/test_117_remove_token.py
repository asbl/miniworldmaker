from miniworldmaker import App, Board, Token, Rectangle, ActionTimer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test117(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                player = Token()
                rectangle = Rectangle(80, 80, 80, 80)
                ActionTimer(20, player.remove, None)
                ActionTimer(40, rectangle.remove, None)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 22, 41]
        QUIT_FRAME = 42
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)



    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()