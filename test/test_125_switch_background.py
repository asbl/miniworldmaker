from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError, timer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test125(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,21, 41, 61]
        QUIT_FRAME = 62
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        board = Board()
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            token = Token()

            board.add_background("images/1.png")
            board.add_background((255, 0, 0, 255))
            board.add_background("images/2.png")

            @timer(frames = 20)
            def switch():
                board.switch_background(0)

            @timer(frames = 40)
            def switch():
                board.switch_background(1)
                
            @timer(frames = 60)
            def switch():
                board.switch_background(2)


        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

