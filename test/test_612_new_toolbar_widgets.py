from miniworldmaker import *
import imgcompare
import os
import unittest
import random
from .helper import screenshot_test

TEST_FRAMES = [1]
QUIT_FRAME = 1
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test612(unittest.TestCase):

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

        toolbar = Toolbar()
        toolbar.margin_left =  20
        toolbar.margin_right = 10
        toolbar.background_color = (0,0,255)



        button = YesNoButton("Yes", "No")
        yes = button.get_yes_button()
        yes.background_color = (0, 255, 0)
        no = button.get_no_button()
        no.background_color = (255, 0, 0)
        toolbar.add_widget(button)

        button2 = Button("test")
        toolbar.add_widget(button2)

        board.add_container(toolbar, "right", size = 300)

        @board.register
        def on_message(self, message):
            print(message)


        """ here are predefined act() and init() methods - delete if used in your testcode"""
        
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
            screenshot_test(self.test_frame, 
                            QUIT_FRAME, 
                            TEST_FRAMES, 
                            self.__class__.__name__,
                            board,
                            self)
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


