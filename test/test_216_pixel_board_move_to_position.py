from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test216(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.columns = 400
                board.rows = 400
                player = Token()
                player.add_costume("images/player_1.png")
                player.position = (200,200)

                @player.register
                def act(self):
                    self.move_towards((280, 260))
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 10, 30, 40, 80]
        QUIT_FRAME = 81
    
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