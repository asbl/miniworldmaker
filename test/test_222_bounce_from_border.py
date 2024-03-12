from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test222(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = Board(150, 150)
            token = Token((50,50))
            token.add_costume("images/ball.png")
            token.direction = 10

            @token.register
            def act(self):
                self.move()
                borders = self.sensing_borders()
                if borders:
                    self.bounce_from_border(borders)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 10, 30, 40, 50, 60, 90]
        QUIT_FRAME = 90
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
