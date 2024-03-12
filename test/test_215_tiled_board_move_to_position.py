from miniworldmaker import App, Board, Token, Position, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test215(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.columns = 8
                board.rows = 8
                board.speed = 30
                player = Token()
                player.add_costume("images/player_1.png")
                player.position = (4, 4)

                @player.register
                def act(self):
                    self.move_towards((7, 7))
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5]
        QUIT_FRAME = 5
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