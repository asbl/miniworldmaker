from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test114(unittest.TestCase):

    def setUp(self):
        def test_code():
            # Here comes your code
            class MyBoard(TiledBoard):
                def setup_environment(self, test):
                    self.columns = 5
                    self.rows = 5
                    self.tile_size = 40
                    self.add_background("images/soccer_green.jpg")
                    self.border_color = (0,0,0,255)
                    token = Token()
                    token.position = (3,4)
                    token.border = 2
                    token.add_costume("images/player.png")
            board = MyBoard()
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

    

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

