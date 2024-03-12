from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test159(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(400,600)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                self.init_test()     
                self.add_background((0,255,0,255))
                self.token = Token((10,10))

                @board.register
                def act_test(self):
                    if self.frame == 20:
                        self.token.x += 100
                    if self.frame == 40:
                        self.reset()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,20,21, 40, 41]
        QUIT_FRAME = 80
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