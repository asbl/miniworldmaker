from miniworldmaker import App, Board, Polygon, Token, Position, Line, Rectangle, Ellipse, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test709(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board((200, 200))
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.default_stroke_color = (0,100,0,100)

                Line((0,0), (100,0))


                l = Line((0,10), (200,10))
                l.border = 1

                l = Line((0,0), (100,100))
                l.border = 4


                l = Line((50,0), (50,200))
                l.border_color = (200,200,0,255)
                l.border = 2

                l = Line((100,0), (100,200))
                l.border_color = (200,200,0,255)
                l.border = 2

                l = Line((100,100), (0,100))
                l.border = 2


                Line((50,100), (160,160))

                l = Line((180,200), (100,2))
                l.border_color = (200,100,0,255)
                l.border = 10

                @l.register
                def act(self):
                    self.start_position = (self.start_position[0], self.start_position[1] + 1)
                    self.end_position = (self.end_position[0], self.end_position[1] + 1)

                l2 = Line((180,220), (100,20))
                l2.border_color = (100,200,0,255)
                l2.border = 10

                @l2.register
                def act(self):
                    self.y += 1
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [0, 20, 40, 60]
        QUIT_FRAME = 60
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