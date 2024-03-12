from miniworldmaker import App, TiledBoard, Token, Position, Circle
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1903(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.grid = True
                circle = Circle((0,0))
                print(circle.position, circle.size)
                @circle.register
                def act(self):
                    self.x += 1
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
