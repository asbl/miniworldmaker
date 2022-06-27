from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,30,60,100,110]
QUIT_FRAME = 110
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test158(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)

        # basiert auf https://github.com/kantel/pygamezero/tree/master/scrolllingbg
        # von 
        WIDTH, HEIGHT = 800, 400
        board = Board(WIDTH, HEIGHT)
        left, bottom = WIDTH/2, HEIGHT/2

        BACKGROUND = "desertback"

        back0 = Token()
        back0.add_costume(BACKGROUND)
        back0.size = WIDTH, HEIGHT
        back1 = Token(WIDTH, 0)
        back1.size = WIDTH, HEIGHT
        back1.add_costume(BACKGROUND)
        backs = [back0, back1]

        walker = Token((100, HEIGHT - 100))
        walker.size = 100, 60
        walker.add_costumes(["walk1", "walk2"])
        walker.speed = 1
        walker.count = 0

        @board.register
        def act(self):
            for back in backs:
                back.x -= 1
                if back.x <= - WIDTH:
                    back.x = WIDTH
            walker.count += walker.speed
            if walker.count > 11:
                costume = walker.next_costume()
                walker.count = 0
            self.test()
        
        @board.register
        def on_key_down(self, keys):
            if "q" in keys:
                board.quit



        """ here act and init - delete if used in testcode"""
        
        @board.register
        def on_setup(self):
            self.init_test()            
            
        #@board.register
        #def act(self):
        #    self.test()
            
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


