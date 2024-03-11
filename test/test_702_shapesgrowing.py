from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1]
QUIT_FRAME = 1
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test702(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)
        shapes = []
        x = 0
        board = Board((800, 600))
        l = Line((0,0), (400, 300))
        shapes.append(l)

        r = Rectangle((400,300),400,300)
        r.center = r.position
        shapes.append(r)

        e = Ellipse((400,300), 80, 30)
        e.position = (0,0)
        shapes.append(e)

        c = Circle((400,300), 20)
        shapes.append(c)

        @board.register
        def act(self):
            r.width = r.width + 1
            c.radius += 1
            l.end_position = (l.end_position[0], l.end_position[1]+1)
            e.height = e.height + 1

        """ here are predefined act() and init() methods - delete if used in your testcode"""
        
        @board.register
        def on_setup(self):
            self.init_test()            
            
        @board.register
        def act(self):
            self.test()
            
        """ here are init_test() and test() methods - They must access the board, so self.board = board is set first""" 
        
        self.board = board
           
        @board.register
        def init_test(self):
            print("setup test")
            board.test_frame = 0
        
        @board.register
        def test(self):
            global TEST_FRAMES
            global QUIT_FRAME
            self.test_frame = self.test_frame + 1
            screenshot_test(self.test_frame, 
                            QUIT_FRAME, 
                            TEST_FRAMES, 
                            board.test_title,
                            board,
                            self)
        
        #in setUp-Method of Test (not Board!):
        board.test_title = self.__class__.__name__
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


