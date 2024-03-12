from miniworldmaker import *
import unittest
import random
from .screenshot_tester import ScreenshotTester

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test706(unittest.TestCase):

    def setUp(self):
        App.reset(unittest = True, file = __file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5,6,7,8]
        QUIT_FRAME = 8
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)

    def test_code():
        """ Should return board """
        App.reset(unittest = True, file = __file__)
        shapes = []

        board = PixelBoard((800, 600))
        l = Line((0,0), (400, 300))
        shapes.append(l)

        r = Rectangle((400,300),400,300)
        r.center = r.position
        shapes.append(r)

        e = Ellipse((400,300), 80, 30)
        e.position = (0,0)
        shapes.append(e)

        p = Polygon([(400,300), (400,450), (600,450)])
        shapes.append(p)
        @board.register
        def act(self):
            for shape in shapes:
                shape.turn_right(1)
        return board

    
    
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


