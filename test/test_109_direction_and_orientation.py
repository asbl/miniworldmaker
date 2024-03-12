from miniworldmaker import *
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test109(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.add_background((0, 0, 0, 100))
                # Token1 at position (2,1) with player costume
                token1 = Token(position=(0, 0))
                token1.add_costume("images/player.png")
                token1.costume.orientation = -90
                assert token1.position == (0,0)
                assert token1.direction == 0
                assert token1.costume.orientation == - 90
                token2 = Token(position=(0, 40))
                token2.add_costume("images/player.png")
                token2.costume.orientation = 90
                token3 = Token(position=(0, 80))
                token3.add_costume("images/player.png")
                token3.costume.orientation = 180
                token4 = Token(position=(0, 120))
                token4.add_costume("images/player.png")
                token4.costume.orientation = 270
                # Unit circle
                token6 = Token(position=(120, 0))
                token6.add_costume("images/player.png")
                token6.costume.orientation = -90
                token6.direction_at_unit_circle = 0
                token7 = Token(position=(120, 40))
                token7.add_costume("images/player.png")
                token7.costume.orientation = -90
                token7.direction_at_unit_circle = 90
                token8 = Token(position=(120, 80))
                token8.add_costume("images/player.png")
                token8.costume.orientation = -90
                token8.direction_at_unit_circle = 180
                token9 = Token(position=(120, 120))
                token9.add_costume("images/player.png")
                token9.costume.orientation = -90
                token9.direction_at_unit_circle = 270
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

