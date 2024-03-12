from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1203(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.background.draw((255,0,0), (200,0), 20, 400)

                for i in range(7):
                    token = Token((10,i*60))
                    token.range = i * 10
                    @token.register
                    def act(self):
                        if not self.sense_color_at(self.direction, self.range) == (255,0,0,255):
                            self.direction = "right"
                            self.move()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,20,40,60,80,120,140,150,170]
        QUIT_FRAME = 170
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
