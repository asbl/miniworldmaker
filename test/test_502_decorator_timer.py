from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test502(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.columns=20
                board.rows=8
                board.tile_size=40
                board.add_background("images/soccer_green.jpg")
                board.add_background("images/space.jpg")
                board.speed = 30

                player = Token(position=(3, 4))
                player.add_costume("images/char_blue.png")
                player.costume.orientation = - 90

                @timer(frames = 24)
                def moving():
                    player.move()

                @loop(frames = 48)
                def moving():
                    player.turn_left()
                    player.move(2)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5,]
        QUIT_FRAME = 5
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


from miniworldmaker import *
import imgcompare
import os
import unittest
import random


    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage
