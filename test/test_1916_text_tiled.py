from miniworldmaker import App, TiledBoard, Token, Position, Text
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1916(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.size = (6,3)
                text = Text((2,1), "Hello")
                text.border = 1
                text.direction = 5
                print("in viewport?", board.camera.is_token_in_viewport(text))
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
