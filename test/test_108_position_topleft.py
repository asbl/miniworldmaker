from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test108(unittest.TestCase):

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
        board = Board(200, 400)
        # Here comes your code
        @board.register
        def act(self):
            board.add_background((100, 0, 0, 255))
            a = Token()
            a.position = (0,0)
            b = Token()
            b.topleft = (100,100)
            c = Token()
            c.position = (200,200)
            d = Token()
            d.center = (250,250)
        """ here act and init - delete if used in testcode"""
        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()
