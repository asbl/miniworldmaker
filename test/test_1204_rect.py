from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1204(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                
                t1 = Token((10,10))
                t1.color = (255,255,255)
                t2 = Token((20,10))
                t2.color = (255,255,255)
                t3 = Token((10,10))
                t3.color = (255,255,255)
                print(t1.get_global_rect())
                print(t2.get_global_rect())
                print(t3.get_global_rect())
                print(t3.sensing_tokens())
                print(t1.sensing_tokens())
                print(t3.sensing_tokens())
                assert(len(t3.sensing_tokens())==2)
                assert(len(t1.sensing_tokens())==2)
                assert(t1 in t3.sensing_tokens())
                assert(t2 in t3.sensing_tokens())
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
