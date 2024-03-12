from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test134b(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                token = Token()
                removed = token.remove_costume()
                assert token.costume_count == 0
                token.add_costume((255,0,0,255))
                assert token.costume_count == 1

            return board
        
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 30
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

        

    def test_main(self):
        print("############ Test MAin ##################")
        with self.assertRaises(SystemExit):
            self.board.run()
