from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
import miniworldmaker
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test701(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = miniworldmaker.Board(800, 600)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                miniworldmaker.Line((0,0), (400, 300))

                e = miniworldmaker.Ellipse((400,300), 400, 300)
                r = miniworldmaker.Rectangle((400,300),400,300)

                r.center = r.position
                r.direction= 5

                l2 = miniworldmaker.Line((0,0), (400, 300))
                l2.start_position = (100,200)

                r2 = miniworldmaker.Rectangle((400,300),40,30)
                r2.center = (0,0)

                r3 = miniworldmaker.Rectangle((400,300),80,30)
                r3.position = (0,0)

                r4 = miniworldmaker.Rectangle((60,120),80,30)
                r4.width = 600

                r5 = miniworldmaker.Rectangle((60,120),80,30)
                r5.height = 600

                e2 = miniworldmaker.Ellipse((400,300), 40, 30)
                e2.center = (0,0)

                e3 = miniworldmaker.Ellipse((400,300), 80, 30)
                e3.position = (0,0)

                e4 = miniworldmaker.Ellipse((60,120),80,30)
                e4.width = 600

                e5 = miniworldmaker.Ellipse((60,120),80,30)
                e5.height = 600
                #board.fill_color=(255,0,0,255)
                p = miniworldmaker.Polygon([(400,300), (400,450), (600,450)])
                p.fill_color = (100,0,0,100)
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

