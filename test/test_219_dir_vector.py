from miniworldmaker import App, Board, Token, Position, Rectangle, Vector
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test219(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(400, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                player = Rectangle((200,200),40, 40)
                player.speed = 1
                player.direction = 80

                @player.register
                def act(self):
                    v1 = Vector.from_token_direction(self)
                    v1.rotate(-1)
                    self.direction = v1
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 20, 40]
        QUIT_FRAME = 41
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