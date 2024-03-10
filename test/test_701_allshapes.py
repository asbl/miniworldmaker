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

class Test701(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)

        import miniworldmaker

        board = miniworldmaker.Board(800, 600)

        miniworldmaker.Line((0,0), (400, 300))

        e = miniworldmaker.Ellipse((400,300), 400, 300)
        r = miniworldmaker.Rectangle((400,300),400,300)

        r.center = r.position
        r.direction= 5

        l2 = miniworldmaker.Line((0,0), (400, 300))
        l2.start_position = (100,200)

        r2 = miniworldmaker.Rectangle((400,300),40,30)
        r2.center = (0,0)

        r3 = miniworldmaker.Rectangle((400,300),80,30)
        r3.position = (0,0)

        r4 = miniworldmaker.Rectangle((60,120),80,30)
        r4.width = 600

        r5 = miniworldmaker.Rectangle((60,120),80,30)
        r5.height = 600

        e2 = miniworldmaker.Ellipse((400,300), 40, 30)
        e2.center = (0,0)

        e3 = miniworldmaker.Ellipse((400,300), 80, 30)
        e3.position = (0,0)

        e4 = miniworldmaker.Ellipse((60,120),80,30)
        e4.width = 600

        e5 = miniworldmaker.Ellipse((60,120),80,30)
        e5.height = 600


        #board.fill_color=(255,0,0,255)
        p = miniworldmaker.Polygon([(400,300), (400,450), (600,450)])
        p.fill_color = (100,0,0,100)




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


