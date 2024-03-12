from miniworldmaker import App, Board, Token, Position, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test214(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                t = Token()
                t.position = (3, 3)
                x = 0
                @board.register
                def act_test(self):
                    nonlocal x
                    x = x + 1
                    if x < 5:
                        t.direction = 135
                        t.move()
                    if x > 5:
                        t.move_in_direction(45)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5,6]
        QUIT_FRAME = 6
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
