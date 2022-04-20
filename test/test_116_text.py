from miniworldmaker import *
import imgcompare
import os
import unittest

TEST_FRAMES = [1]
QUIT_FRAME = 25
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test116(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = PixelBoard()
        board.size = (600,300)

        t1 = Text((50,100), "Hello World 1")
        t1.border = 1
        t1.font_size = 50
        t1.direction = 5

        t2 = Text((0,0), "Hello World 2")
        t2.border = 1
        t2.font_size = 20
        t2.position = (50,50)

        t3 = Text((0,0))
        t3.text = "Hello World 3"
        t3.border = 1
        t3.font_size = 20
        t3.position = (50,200)

        t4 = Text((0,0))
        t4.text = "Hello World 4"
        t4.border = 1
        t4.color = (255,100,100,100)
        t4.font_size = 20
        t4.position = (20,280)


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
                file_test = path + f'output/{self.test_title}_test.png'
                file_output = path + f"output/{self.test_title}.png"
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

