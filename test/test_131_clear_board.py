from miniworldmaker import App, Board, Token, Position, timer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test131(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                for i in range(50):
                    Token((random.randint(0,board.width), random.randint(0,board.height)))

                @timer(frames = 10)
                def clean():
                    board.clear()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [11]
        QUIT_FRAME = 12
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()