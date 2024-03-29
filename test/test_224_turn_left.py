from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test224(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = Board(100, 100)
                t = Token()
                t.add_costume("images/arrow.png")
                t.size = (100,100)

                @t.register
                def act(self):
                    t.turn_left(1)
            return board
            
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,10,20]
        QUIT_FRAME = 20
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