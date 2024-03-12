from miniworldmaker import App, PixelBoard, Polygon, Token, Position, Line, Rectangle, Ellipse, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test707(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard((200, 200))
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.default_fill_color = (255,255,255,100)

                Circle((100,100), 50)

                board.default_fill_color = (255,0,0,100)
                b = Circle.from_topleft((100,100),50)
                b.direction = 10
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
