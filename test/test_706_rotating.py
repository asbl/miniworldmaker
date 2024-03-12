from miniworldmaker import App, PixelBoard, Polygon, Token, Position, Line, Rectangle, Ellipse, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test706(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard((800, 600))
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                shapes = []
                l = Line((0,0), (400, 300))
                shapes.append(l)

                r = Rectangle((400,300),400,300)
                r.center = r.position
                shapes.append(r)

                e = Ellipse((400,300), 80, 30)
                e.position = (0,0)
                shapes.append(e)

                p = Polygon([(400,300), (400,450), (600,450)])
                shapes.append(p)
                @board.register
                def act_test(self):
                    for shape in shapes:
                        shape.turn_right(1)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5,6,7,8]
        QUIT_FRAME = 8
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