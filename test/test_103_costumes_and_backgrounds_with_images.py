from miniworldmaker import *
import os
import unittest
import random
from .screenshot_tester import ScreenshotTester


def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage


class Test103(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)

        App.reset(unittest=True, file=__file__)

    def test_code(self):
        board = TiledBoard()
        # Black board
        board.add_background((200, 200, 200, 255))
        board.columns = 5
        board.rows = 5
        board.tile_size = 40

        # Token1 at position (2,1) with player costume
        token1 = Token(position=(2, 1))
        token1.add_costume("images/player.png")
        print(token1.costumes, token1.costume.images)
        # Token2 at position (3,1) with purple background
        token2 = Token(position=(3, 1))
        token2.add_costume((100, 0, 100, 100))
        try:
            token2.size = (1, 1)
        except Exception as e:
            print(e)
        token2.position = (40, 40)

        token2 = Token(position=(3, 2))
        token2.add_costume((100, 0, 100, 100))

        token3 = Token(position=(3, 2))
        token3.add_costume("images/player.png")
        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()
