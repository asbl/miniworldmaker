from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test112(unittest.TestCase):

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
        board = Board(200, 200)
        # Here comes your code
        @board.register
        def setup_environment(self, test):
            board.default_fill_color = (0,255,255,255)

        token = Text((0,0), "Hello World!")
        token.auto_size = "font"

        token2 = Text((0,60))
        token2.set_text("Hello!")
        token2.auto_size = "token"
        token2.font_size = 32

        token3 = Number((0,150))
        token3.auto_size = None
        token3.font_size=64

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()

