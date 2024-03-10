from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,3,6,9,12,20,40,60]
QUIT_FRAME = 60
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test718(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)
        
        board = PhysicsBoard(400,400)

        for i in range(9):
            l = Line((i*40,20+i*10),((i+1)*40,20+i*10))
            l.thickness = i
            

        for i in range(9):
            l = Line((i*40,80+i*10),((i+1)*40,120+i*10))
            l.thickness = i
            
        for i in range(9):
            l = Line((i*40,160+i*10),((i+1)*40,160+i*10))
            l.thickness = i
            l.direction = 135


        for i in range(18):
            l = Line((300,300),(350,350))
            l.direction = i * 20
            l.border_color = (i * 10, i *10, i* 10)
            
        l =Line((100,300), (150,300))
        @l.register
        def act(self):
            l.direction+=1
            

        board.debug = True




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


