from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test110(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        board = Board()
        # Here comes your code
        import pygame
        # Black board
        @board.register
        def setup_environment(self, test):
            board.add_background((0, 0, 0, 100))
            board.size = (400, 300)
            # tokens looking:
            # * up(dir 0, or:-90)
            # * down(dir 0, or:90)
            # * left(dir 0, or:180)
            # * right(dir 0, or:270)

            # Token1 at position (2,1) with player costume
            token1 = Token(position=(0, 50))
            token1.add_costume("images/player.png")
            token1.costume.orientation = -90
            assert token1.position == Position(0, 50)
            assert token1.direction == 0
            assert token1.orientation == -90

            token2 = Token(position=(0, 100))
            token2.add_costume("images/player.png")
            token2.costume.orientation = 90
            token3 = Token(position=(0, 150))
            token3.add_costume("images/player.png")
            token3.costume.orientation = 180
            token4 = Token(position=(0, 200))
            token4.add_costume("images/player.png")
            token4.costume.orientation = 270

            assert token4.position == Position(0, 200)
            #assert token4.rect == pygame.Rect(0, 200, 40, 40)

            class UpToken(Token):
                def on_setup(self):
                    self.direction = 0
                    self.costume.orientation = -90

            class LeftToken(Token):
                def on_setup(self):
                    self.direction = -90
                    self.costume.orientation = -90

            class DownToken(Token):
                def on_setup(self):
                    self.direction = 180
                    self.costume.orientation = -90

            class RightToken(Token):
                def on_setup(self):
                    self.costume.orientation = -90
                    self.direction = 90
                    


            r = RightToken(position=(50, 50))
            r.add_costume("images/player.png")
            l = LeftToken(position=(50, 100))
            l.add_costume("images/player.png")
            u = UpToken(position=(50, 150))
            u.add_costume("images/player.png")
            d = DownToken(position=(50, 200))
            d.add_costume("images/player.png")
        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

