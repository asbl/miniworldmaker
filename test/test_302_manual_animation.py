from miniworldmaker import App, Board, Token, Position, ActionTimer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test302(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = Board(280, 100)
                board.add_background("images/water.png")
                board.speed = 1

                robo = Token(position=(0, 0))
                robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
                ActionTimer(80,robo.costume.set_image,1)
                ActionTimer(120,robo.costume.set_image,2)
                ActionTimer(150,robo.costume.set_image,3)
                robo.costume.animation_speed = 200
            return board

        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 20, 40, 60, 80, 100, 120]
        QUIT_FRAME = 121
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

