from miniworldmaker import App, Board, Token, Position, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test201(unittest.TestCase):

    def setUp(self):
        def test_code():
            board=TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                
                board.columns = 4
                board.rows = 1
                board.speed = 20
                fish = Token()
                fish.border = 1
                fish.add_costume("images/fish.png")
                fish.direction = "right"
                fish.orientation = -90
                @fish.register
                def act(self):
                    self.move()

                @fish.register
                def on_sensing_not_on_board(self):
                    self.move_back()
                    self.flip_x()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5,6,7,8]
        QUIT_FRAME = 8
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()