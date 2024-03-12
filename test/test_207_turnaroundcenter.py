from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test207(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard(200,200)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                import pygame
                board.add_background((0,0,0,255))
                # Output should be a cross, not an inverted L!
                tkn = Token()
                tkn.position = (50,50)
                tkn.add_costume((255,255,255,100))
                tkn.size= (10, 100)
                print("tkn1, position, center, ", tkn.position, tkn.center, tkn.rect, tkn.costume.image)
                assert(tkn.position == Position(50,50))
                assert(tkn.center == Position(55,100))
                assert(tkn.rect == pygame.Rect(50,50,10,100))

                tkn2 = Token()
                tkn2.position = (50,50)
                tkn2.add_costume((0,255,255,100))
                tkn2.size= (10, 100)
                #print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect)
                assert tkn2.position == Position(50,50)
                assert tkn2.center == Position(55,100)
                tkn2.turn_left(90)
                #print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect)
                assert tkn2.position == Position(50, 50)
                assert tkn2.center == Position (55, 100)
                assert tkn2.size == (10, 100)
                # print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect, tkn2.size, tkn2.rect)
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