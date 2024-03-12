from miniworldmaker import *
import imgcompare
import os
import unittest
from .screenshot_tester import ScreenshotTester

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test105(unittest.TestCase):
    def setUp(self):
        def test_code():
            board = PixelBoard(400,300)
            @board.register
            def setup_environment(self, test):
                board.add_background("images/grass.jpg")
                board.size = (800,300)
                board.background.is_scaled_to_width = True
                # 4 tokens: In topleft corner, at (20,20)
                t1 = Token(position=(0, 0))
                t2 = Token(position=(60, 40))
                t2.add_costume("images/char_blue.png")
                t3 = Token(position=(100, 40))
                t3.add_costume("images/char_blue.png")

                t4 = Token()
                t4.center=(20, 20)
                t4.add_costume((100,100,100,200))
                test.assertEqual(t4.position, Position(0,0))
                test.assertEqual(t4.center, Position(20,20))
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if (hasattr(board, "setup_environment")):
            board.setup_environment(self)

        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


