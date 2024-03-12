from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test140(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                token = Token()
                token.remove_costume()
                assert token.costume_count == 0
                token.add_costume((255,0,0))
                assert token.costume_count == 1
                token.add_costume((0,255,0))
                print(token.costumes)
                assert token.costume_count == 2
                token.remove_costume()
                print(token.costumes)
                assert token.costume_count == 1
                token.remove_costume()
                assert token.costume_count == 0
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
