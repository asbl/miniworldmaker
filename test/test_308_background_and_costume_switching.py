from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1, 5, 10, 15, 20]
QUIT_FRAME = 21
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test308(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)


        board = Board()
        board.add_background("images/1.png")
        board.background.add_image("images/2.png")

        bg3 = board.add_background("images/3.png")
        bg4 = board.add_background("images/4.png")
        bg4.add_image("images/5.png")

        token = Token()
        token.add_costume("images/1.png")
        token.costume.add_image("images/2.png")

        c3 = token.add_costume("images/3.png")
        c4 = token.add_costume("images/4.png")
        c4.add_image("images/5.png")

            
        @timer(frames = 20)
        def do():
            board.switch_background(1)
            token.switch_costume(1)

        @timer(frames = 40)
        def do():
            board.switch_background(0)
            token.switch_costume(0)

        @timer(frames = 60)
        def do():
            board.background.set_image(1)
            token.costume.set_image(1)
            
        @timer(frames = 80)
        def do():
            board.background.from_appearance(bg4, 0)
            token.costume.from_appearance(c4, 0)
            board.background.set_image(1)
            token.costume.set_image(1)
    
       
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


