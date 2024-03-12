from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test213(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard(200,200)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                import pygame
                player1 = Token(position=(0, 0))
                player1.size = (40, 40)
                player1.add_costume("images/char_blue.png")
                player1.costume.orientation = 0

                player2 = Token(position=(40, 0))
                player2.size = (40, 40)
                player2.add_costume("images/char_blue.png")
                player2.costume.orientation = - 90

                player3 = Token(position=(80, 0))
                player3.size = (40, 40)
                player3.add_costume("images/char_blue.png")
                player3.costume.orientation = 180

                player4 = Token(position=(120, 0))
                player4.size = (40, 40)
                player4.add_costume("images/char_blue.png")
                player4.costume.orientation = 90

                class Player5(Token):
                    def on_setup(self):
                        self.size = (40, 40)
                        self.add_costume("images/char_blue.png")
                        self.costume.orientation = 90
                        
                player5 = Player5(position = (160,0))
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