from miniworldmaker import App, Board, Token, Position, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test225(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(800, 600)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                a = Circle()
                a.direction  = 45
                assert(a.direction == 45)
                assert(a.direction_at_unit_circle == 45)
                a.direction  = 0
                assert(a.direction == 0)
                assert(a.direction_at_unit_circle == 90)
                a.direction  = -90
                assert(a.direction == -90)
                print(a.direction_at_unit_circle)
                assert(a.direction_at_unit_circle == -180)
                a.direction = 180
                print(a.direction)
                assert(abs(a.direction) == 180)
                assert(a.direction_at_unit_circle == -90)

                a.direction_at_unit_circle = -90
                assert(abs(a.direction) == 180)
                print(a.direction_at_unit_circle)
                assert(a.direction_at_unit_circle == -90)

                a.direction_at_unit_circle = -180
                print(a.direction)
                assert(a.direction == -90)
                print(a.direction_at_unit_circle)
                assert(a.direction_at_unit_circle == -180)
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
