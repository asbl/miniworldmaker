from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1, 20, 40, 60, 80, 100, 120]
QUIT_FRAME = 121
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test301(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """



        board = PixelBoard(columns=280, rows=100)
        board.add_background("images/water.png")
        board.speed = 1
        print(board.speed, board.fps)
        robo = Token(position=(0, 0))
        robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
        print(robo.costume)
        robo.size = (99, 99)
        robo.costume.loop = True
        robo.costume.animate()
        robo.costume.orientation = - 90
        robo.costume.animation_speed = 20
        robo.direction = "right"
        @robo.register
        def act(self):
            if self.sensing_on_board():
                self.move()
        @robo.register
        def on_sensing_not_on_board(self):
            self.flip_x()
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

