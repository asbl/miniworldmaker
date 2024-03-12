from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test220(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                token = Token()
                token.add_costume("images/alien1.png")
                token.height= 400
                token.width = 100
                token.is_rotatable = False
                @token.register
                def act(self):
                    if self.board.frame % 20 == 0:
                        print("flip")
                        if self.costume.is_flipped:
                            self.costume.is_flipped = False
                        else:
                            self.costume.is_flipped = True
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 21, 41]
        QUIT_FRAME = 41
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