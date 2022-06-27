from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,2,3,4,6,8,10,12,14,16,18,20,22,30,40,60,80,100,120,140,160]
QUIT_FRAME = 161
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test303(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)



        board = Board(280, 100)
        board.add_background("images/water.png")
        board.speed = 1
        # Should show: A1, B1, C1, C2, C3, A1
        robo = Token(position=(0, 0))

        costume_a = robo.add_costume(["images/a1.png","images/a2.png","images/a3.png"])
        costume_b = robo.add_costume(["images/b1.png","images/b2.png","images/b3.png"])
        costume_c = robo.add_costume(["images/c1.png","images/c2.png","images/c3.png"])
        @costume_c.register
        def after_animation(self):
            self.token.switch_costume(costume_a)
            print("after animation")
        robo.size = (99, 99)

        costume_a.animation_speed = 80
        costume_b.animation_speed = 80
        costume_c.animation_speed = 80

        ActionTimer(30,robo.animate_costume,costume_b)
        ActionTimer(90,robo.animate_costume,costume_c)
        robo.costume.animate()


    
       
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


