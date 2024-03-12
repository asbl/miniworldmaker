from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test301(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard(280, 100)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.add_background("images/water.png")
                board.speed = 1
                print(board.speed, board.fps)
                robo = Token(position=(0, 0))
                robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
                print(robo.costume)
                robo.size = (99, 99)
                robo.costume.loop = True
                robo.costume.animate()
                robo.costume.orientation = - 90
                robo.costume.animation_speed = 20
                robo.direction = "right"
                @robo.register
                def act(self):
                    if self.sensing_on_board():
                        self.move()
                @robo.register
                def on_sensing_not_on_board(self):
                    self.flip_x()
                    self.move()
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