from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test136(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 2, 3, 4, 5, 6]
        QUIT_FRAME = 7
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        board = Board((100,60))
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            token = Token((10,10))
            board.speed = 30
            costume1 = token.add_costume((255,255,0))
            costume2 = token.add_costume((255,0,255))
            @token.register
            def act(self):
                print(costume1, costume2)
                if self.costume == costume1:
                    self.switch_costume(costume2)
                else:
                    self.switch_costume(costume1)

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

