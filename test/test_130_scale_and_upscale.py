from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test130(unittest.TestCase):

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
        board = Board(800,400)
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            def create_player(x, y):
                t = Token()
                t.position = (x, y)
                t.add_costume("images/player.png")
                t.border = 1
                return t

            t = create_player(0,180)
            t.size=(80,80)

            t = create_player(80,180)
            t.costume.is_upscaled = True
            t.size=(80,80)

            t = create_player(160,180)
            t.costume.is_scaled = True
            t.size=(80,80)

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()