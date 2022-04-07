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

class Test207(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """

        import pygame
        board = PixelBoard(200,200)
        board.add_background((0,0,0,255))
        # Output should be a cross, not an inverted L!
        tkn = Token()
        tkn.position = (50,50)
        tkn.add_costume((255,255,255,100))
        tkn.size= (10, 100)
        print("tkn1, position, center, ", tkn.position, tkn.center, tkn.rect, tkn.costume.image)
        assert(tkn.position == Position(50,50))
        assert(tkn.center == Position(55,100))
        assert(tkn.rect == pygame.Rect(50,50,10,100))

        tkn2 = Token()
        tkn2.position = (50,50)
        tkn2.add_costume((0,255,255,100))
        tkn2.size= (10, 100)
        print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect)
        assert tkn2.position == Position(50,50)
        assert tkn2.center == Position(55,100)
        tkn2.turn_left(90)
        assert tkn2.position == Position(50, 50)
        assert tkn2.center == Position(55, 100)
        assert(tkn2.rect == pygame.Rect(5,94,100,12))
        print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect, tkn2.size, tkn2.rect)





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


