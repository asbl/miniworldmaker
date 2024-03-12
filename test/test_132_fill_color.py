from miniworldmaker import App, Board, Token, Position, Circle, Ellipse
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test132(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200,80)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.default_fill_color = (0,0, 255)

                t = Token()

                t2 = Token((40,0))
                t2.is_filled = (0, 255, 0)

                t3 = Token((80, 0))
                t3.fill_color = (255, 0, 0)

                t4 = Token((120, 0))
                t4.add_costume((0,0,0))
                t4.fill_color = (255, 255, 0)

                t5 = Token((160, 0))
                t5.add_costume("images/player.png")
                t5.fill_color = (255, 255, 0, 100) # image is overwritten
                assert (t5.is_filled == (255, 255, 0, 100))

                t6 = Circle((0, 40), 20)
                t6.position = t6.center
                t6.fill_color = (255, 255, 255)

                t7 = Ellipse((40, 40), 40, 40)
                t7.fill_color = (255, 0, 255) 

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