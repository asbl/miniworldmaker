from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test304(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(80,40)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                robo = Token()
                robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
                robo.costume.animation_speed = 20
                robo.costume.animate()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [110,20,30,40,50,60,70,80]
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