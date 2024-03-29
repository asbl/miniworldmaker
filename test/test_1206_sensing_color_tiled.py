from miniworldmaker import App, TiledBoard, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1206(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard(6,6)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                assert board.rows == 6
                assert board.columns == 6
                for x in range(board.rows):
                    for y in range(board.columns):
                        color = (x * y) / (board.rows * board.columns) * 255
                        board.background.draw((color, color, color), (x * board.tile_size,y * board.tile_size), 40,40)
                token = Token((3,3))
                print(token.sensing_color((63,63,63)))
                print(token.sense_color_at(distance = 1, direction = 90))
                assert(token.sensing_color((63,63,63)) is True)
                assert(token.sense_color_at(distance = 1, direction = 90) == (85,85,85,255) )
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
