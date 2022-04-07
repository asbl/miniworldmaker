from miniworldmaker import *
import imgcompare
import os
import unittest

TEST_FRAMES = [1, 41, 81, 121]
QUIT_FRAME = 122
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test125b(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = Board(120,60)
        t1 = Token()
        costume =t1.add_costume("images/1.png")
        t1.add_costume("images/2.png")
        t1.switch_costume(1)

        t2 = Token((40,0))
        t2.add_costume((100,0,0))
        t2.add_costume((0,100,0))

        @timer(frames = 40)
        def switch():
            print("switch t1")
            t1.switch_costume(0)

        @timer(frames = 80)
        def switch():
            print("switch t2")
            t2.switch_costume(0)
            print("switch t3")
            t3.switch_costume(0)

            
        @timer(frames = 120)
        def switch():
            print("switch t2")
            t2.switch_costume(1)
            print("switch t3")
            t3.switch_costume(1)
            

        t3 = Token((80,0))
        t3.add_costume("images/1.png")
        t3.add_costume("images/2.png")






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


