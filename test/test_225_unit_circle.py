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

class Test225(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """


        board = Board((800, 600))

        a = Circle()
        a.direction  = 45
        assert(a.direction == 45)
        assert(a.direction_at_unit_circle == 45)
        a.direction  = 0
        assert(a.direction == 0)
        assert(a.direction_at_unit_circle == 90)
        a.direction  = -90
        assert(a.direction == -90)
        print(a.direction_at_unit_circle)
        assert(a.direction_at_unit_circle == -180)
        a.direction = 180
        print(a.direction)
        assert(abs(a.direction) == 180)
        assert(a.direction_at_unit_circle == -90)

        a.direction_at_unit_circle = -90
        assert(abs(a.direction) == 180)
        print(a.direction_at_unit_circle)
        assert(a.direction_at_unit_circle == -90)

        a.direction_at_unit_circle = -180
        print(a.direction)
        assert(a.direction == -90)
        print(a.direction_at_unit_circle)
        assert(a.direction_at_unit_circle == -180)
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

