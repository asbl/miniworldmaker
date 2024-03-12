from miniworldmaker import App, PixelBoard, Token, Text
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test116(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = PixelBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = PixelBoard()
                board.size = (600,300)

                t1 = Text((50,100), "Hello World 1")
                t1.border = 1
                t1.font_size = 50
                t1.direction = 5

                t2 = Text((0,0), "Hello World 2")
                t2.border = 1
                t2.font_size = 20
                t2.position = (50,50)

                t3 = Text((0,0))
                t3.text = "Hello World 3"
                t3.border = 1
                t3.font_size = 20
                t3.position = (50,200)

                t4 = Text((0,0))
                t4.text = "Hello World 4"
                t4.border = 1
                t4.color = (255,100,100,100)
                t4.font_size = 20
                t4.position = (20,280)
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


    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()

