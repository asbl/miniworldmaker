from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test212(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                # Is player 1 sensing player 2? Should return True
                import pygame
                board.columns=300
                board.rows=200
                board.add_background("images/soccer_green.jpg")
                board.add_background("images/space.jpg")
                board.speed = 30

                player1 = Token(position=(30, 4))
                player1.size = (40, 40)
                player1.add_costume("images/char_blue.png")
                player1.costume.orientation = - 90

                player2 = Token(position=(3, 4))
                player2.size = (40, 40)
                player2.add_costume("images/char_blue.png")
                player2.costume.orientation = - 90

                player3 = Token(position=(90, 4))
                player3.size = (40, 40)
                player3.add_costume("images/char_blue.png")
                player3.costume.orientation = - 90

                @player1.register
                def act(self):
                        assert(player1.rect == pygame.Rect(30, 4, 40, 40))


                @player2.register
                def act(self):
                    assert(player2.rect == pygame.Rect(3, 4, 40, 40))

                @player1.register
                def on_sensing_token(self, token):
                    assert(token==player2)
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