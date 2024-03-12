from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test124(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(800,400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                def create_token(x, y):
                    t = Token()
                    t.position = (x, y)
                    t.add_costume("images/alien1.png")
                    t.border = 1
                    return t

                t0 = create_token(0,0)
                assert(t0.width == 40)
                assert(t0.height == 40)

                t1 = create_token(50,0)
                t1.height = 400
                assert(t1.height==400)
                assert(t1.width==40)
                t2 = create_token(300,0)
                t2.width = 180
                assert(t2.width==180)
                assert(t2.height==40)

                t = Token((600,50))
                t.add_costume("images/alien1.png")
                t.costume.is_scaled = True
                t.size = (140,80)
                t.border = 1
                assert(t.width==140)
                assert(t.height==80)

                t = Token((600,150))
                t.add_costume("images/alien1.png")
                t.costume.is_upscaled = True
                t.border = 1
                assert (t.width, t.height) == (40,40)

                t = Token((650,150))
                t.add_costume("images/alien1.png")
                t.costume.is_upscaled = True
                t.border = 1
                t.size = (140,80)
                assert t.width, t.height == (140,80)

                t = Token((600,250))
                t.add_costume("images/alien1.png")
                t.costume.alpha = 50
                t.width = 40
                t.border = 1
                assert t.width, t.height == (40,40)
                
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


if __name__ == "__main__":
    unittest.main()