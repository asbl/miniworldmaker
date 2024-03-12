from miniworldmaker import *
import imgcompare
import os
import unittest
from .screenshot_tester import ScreenshotTester

class Test104(unittest.TestCase):
    
    def setUp(self):
        def test_code():
            board = PixelBoard(400,300)
            
            @board.register
            def setup_environment(self):
                board.add_background("images/stone")

                token1 = Token()
                token1.add_costume("images/player")
                token1.position = (20,20)
                try:
                    token2 = Token()
                    token2.position = (120,120)
                    token2.add_costume("images/player.gif")
                except Exception as e:
                    print(e)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if (hasattr(board, "setup_environment")):
            board.setup_environment()
        
    

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == '__main__':
    unittest.main()


