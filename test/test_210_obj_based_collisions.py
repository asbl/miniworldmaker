from miniworldmaker import App, Board, Token, Position, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test210(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.columns=5
                board.rows=5
                board.tile_size=40
                board.add_background("images/soccer_green.jpg")
                board.add_background("images/space.jpg")
                board.speed = 30

                player1 = Token(position=(3, 4))
                player1.add_costume("images/char_blue.png")
                player1.costume.orientation = - 90

                @player1.register
                def on_sensing_token(self, token):
                    if token == player2 and self.board.frame == 1:
                        assert(token == player2)

                player2 = Token(position=(3, 4))
                player2.add_costume("images/char_blue.png")
                player2.costume.orientation = - 90
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
