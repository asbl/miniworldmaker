from miniworldmaker import App, Board, Token, Position, Line, Rectangle, Ellipse, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test702(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board((800, 600))
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                shapes = []
                x = 0
                
                l = Line((0,0), (400, 300))
                shapes.append(l)

                r = Rectangle((400,300),400,300)
                r.center = r.position
                shapes.append(r)

                e = Ellipse((400,300), 80, 30)
                e.position = (0,0)
                shapes.append(e)

                c = Circle((400,300), 20)
                shapes.append(c)

                @board.register
                def act(self):
                    r.width = r.width + 1
                    c.radius += 1
                    l.end_position = (l.end_position[0], l.end_position[1]+1)
                    e.height = e.height + 1
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

