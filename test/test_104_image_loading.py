from miniworldmaker import *
import imgcompare
import os
import unittest
from .screenshot_tester import ScreenshotTester

class Test104(unittest.TestCase):
    
    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if (hasattr(board, "setup_environment")):
            board.setup_environment()
        
    def test_code(self):
        board = PixelBoard(400,300)
        self.board = board
        path = os.path.dirname(__file__)
        board.app.register_path(path)
            
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

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()

        
        
    def test_102(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


