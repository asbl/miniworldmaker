from miniworldmaker import *
import imgcompare
import os
import unittest

TEST_FRAMES = [1]
QUIT_FRAME = 1
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test124(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = Board(800,400)

        def create_token(x, y):
          t = Token()
          t.position = (x, y)
          t.add_costume("images/alien1.png")
          t.border = 1
          return t

        t0 = create_token(0,0)
        assert(t0.width == 40)
        assert(t0.height == 40)

        t1 = create_token(50,0)
        t1.height = 400
        assert(t1.height==400)
        assert(t1.width==400)
        t2 = create_token(300,0)
        t2.width = 180
        assert(t2.width==180)
        assert(t2.height==180)

        t = Token((600,50))
        t.add_costume("images/alien1.png")
        t.costume.is_scaled = True
        t.size = (140,80)
        t.border = 1
        assert(t.width==140)
        assert(t.height==80)

        t = Token((600,150))
        t.add_costume("images/alien1.png")
        t.costume.is_upscaled = True
        t.border = 1
        assert(t.width, t.height == (40,40))

        t = Token((650,150))
        t.add_costume("images/alien1.png")
        t.costume.is_upscaled = True
        t.border = 1
        t.size = (140,80)
        assert(t.width, t.height == (140,80))

        t = Token((600,250))
        t.add_costume("images/alien1.png")
        t.costume.alpha = 50
        t.width = 40
        t.border = 1
        assert(t.width, t.height == (40,40))


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
        
        
    def test_108(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


