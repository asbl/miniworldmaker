from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test305(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                token = Token()
                costume = token.add_costume("images/1.png")
                costume.add_image("images/2.png")
                costume.animate()
                @costume.register
                def after_animation(self):
                    self.parent.remove()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 10, 30]
        QUIT_FRAME = 31
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