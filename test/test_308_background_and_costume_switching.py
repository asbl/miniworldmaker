from miniworldmaker import App, Board, Token, Position, timer
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test308(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.add_background("images/1.png")
                board.background.add_image("images/2.png")

                bg3 = board.add_background("images/3.png")
                bg4 = board.add_background("images/4.png")
                bg4.add_image("images/5.png")

                token = Token()
                token.add_costume("images/1.png")
                token.costume.add_image("images/2.png")

                c3 = token.add_costume("images/3.png")
                c4 = token.add_costume("images/4.png")
                c4.add_image("images/5.png")

                    
                @timer(frames = 20)
                def do():
                    board.switch_background(1)
                    token.switch_costume(1)

                @timer(frames = 40)
                def do():
                    board.switch_background(0)
                    token.switch_costume(0)

                @timer(frames = 60)
                def do():
                    board.background.set_image(1)
                    token.costume.set_image(1)
                    
                @timer(frames = 80)
                def do():
                    board.background.from_appearance(bg4, 0)
                    token.costume.from_appearance(c4, 0)
                    board.background.set_image(1)
                    token.costume.set_image(1)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 5, 10, 15, 20]
        QUIT_FRAME = 21
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