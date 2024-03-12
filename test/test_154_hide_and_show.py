from miniworldmaker import App, Board, Token, Position, TiledBoard, timer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test154(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = TiledBoard(2,2)
                token = Token()

                @timer(frames = 12)
                def hide():
                    token.hide()

                @timer(frames = 48)
                def show():
                    token.show()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [0, 1, 2]
        QUIT_FRAME = 3
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