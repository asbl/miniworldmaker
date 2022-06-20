from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,20,40,60,80,120,140,150,170]
QUIT_FRAME = 170
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test1205(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = Board()
        wall=Token((200,0))
        wall.color = (255,255,255)
        wall.size = (20, 400)

        for i in range(7):
            token = Token((10,i*60))
            token.color = (255,255,255)
            token.range = i * 10
            token.number = i % 4
            @token.register
            def act(self):
                if self.number == 0:
                    if not self.sensing_token(wall):
                        self.direction = "right"
                        self.move()
                if self.number == 1:
                    if not self.sensing_token():
                        self.direction = "right"
                        self.move()
                if self.number == 2:
                    if not self.sensing_tokens():
                        self.direction = "right"
                        self.move()
                if self.number == 3:
                    if not self.sensing_tokens(wall):
                        self.direction = "right"
                        self.move()
                    

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


