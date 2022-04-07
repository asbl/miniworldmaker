from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,2,3,4,5,6,7,8]
QUIT_FRAME = 8
    
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








        """ here act and init - delete if used in testcode"""
        
        @board.register
        def on_setup(self):
            self.init_test()            
            
        @board.register
        def act(self):
            self.test()
            
        """ end of setUp - code up here""" 
        
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
            if self.test_frame in TEST_FRAMES:
                print("screenshot test at frame",  self.test_frame)
                path = os.path.dirname(__file__)
                if path != "":
                    path =  path + "/"
                file_test = path + f'output/{self.test_title}_test_{self.test_frame}.png'
                file_output = path + f"output/{self.test_title}_{self.test_frame}.png"
                if not os.path.isfile(file_test):
                    board.screenshot(file_test)
                board.screenshot(file_output)
                d = diff(file_test, file_output)
                assert 0 <= d <= 0.05
            if self.test_frame == QUIT_FRAME:
                self.quit()
        
        #in TESTXYZ setup:
        board.test_title = self.__class__.__name__
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


