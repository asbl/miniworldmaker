from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test208(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 200)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                tkn = Token((0,0))
                tkn.move_right(1)
                tkn2 = Token((0,40))
                tkn2.move_right(40)
                tkn3 = Token((0,80))
                tkn3.move_right(80)
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
