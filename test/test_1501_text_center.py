from miniworldmaker import App, Board, Token, Position, Text, Line
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1501(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(640, 500)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                Line((320,0), (320, 500))

                t1 = Text((100,100), "Test1")
                print(t1.width)
                t1.text = "Test1: " + str(t1.width)
                print(t1.width)
                t1.x = (board.width - t1.width) / 2
                t1.border = 1

                t2 = Text((100,150), "Test2")
                t2.text = "Test2: " + str(t2.width)
                t2.font_size = 50
                t2.x = (board.width - t2.width) / 2
                t2.border = 1
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


if __name__ == "__main__":
    unittest.main()