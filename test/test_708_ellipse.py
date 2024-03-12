from miniworldmaker import App, PixelBoard, Polygon, Token, Position, Line, Rectangle, Ellipse, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test708(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard((200, 200))
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.default_fill_color = (255,255,255,100)

                Ellipse((0,100), 200, 100)

                board.default_fill_color = (255,0,0,100)
                Ellipse.from_center((100,100),20, 10)

                board.default_fill_color = (0,255,0,100)
                e = Ellipse((100,100),10, 10)
                e.center = e.position

                board.default_fill_color = (0,255,0,50)
                e = Ellipse((100,100),18.1, 18.1)
                e.center = e.position
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