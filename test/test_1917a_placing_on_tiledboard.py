from miniworldmaker import App, TiledBoard, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1917a(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.add_background("images/soccer_green.jpg")
                board.columns=20
                board.rows=8
                board.tile_size=40
                board.background.grid = True

                player = Token(position=(3, 4))
                player.add_costume("images/char_blue.png")
                player.border = 1
                print(player.size)
                print(player.position, player.direction)
                print(player.image)
                player.orientation = -90
                @player.register
                def on_key_down(self, key):
                    self.move()
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
