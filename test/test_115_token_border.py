from miniworldmaker import App, TiledBoard, Token
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test115(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        class MyBoard(TiledBoard):
            def setup_environment(self, test):
                self.columns = 5
                self.rows = 5
                self.tile_size = 40
                self.add_background("images/soccer_green.jpg")
                self.default_border_color = (255,100,100,255)
                self.default_border = 5
                
                token = Token()
                token.position = (0, 0)
                token.add_costume((100, 100, 100))
                
                token2 = Token()
                token2.fill = True
                token2.fill_color = (0,100,0)
                token2.border = 10
                token2.costume.stroke_color = (0,200,0)
                token2.position = (1, 0)
                
                token = Token()
                token.costume.add_image((0,200,200))
                token.position = (2, 0)
                self.init_test()
            
        board = MyBoard(8, 6)
        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()


