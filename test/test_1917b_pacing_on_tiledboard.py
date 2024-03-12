from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1917(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.add_background("images/grass.jpg")
                board.columns=20
                board.rows=8
                board.tile_size=40

                player = Token(position=(3, 4))
                player.add_costume("images/char_blue.png")
                test.assertEquals(player.position, Position(3, 4))
                test.assertEquals(player.direction, 0)
                player.orientation = -90
                test.assertEquals(player.direction, 0)
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


