from miniworldmaker import App, Board, Token, Position, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test230(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(100, 100)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                t = Circle((50,50))
                @t.register
                def act(self):
                    self.x += 1
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,20,30,40,50,60,70]
        QUIT_FRAME = 70
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
