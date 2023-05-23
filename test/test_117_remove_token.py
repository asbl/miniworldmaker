from miniworldmaker import Board, Token, Rectangle, ActionTimer, App
import imgcompare
import os
import unittest

TEST_FRAMES = [1, 22, 41]
QUIT_FRAME = 42
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test117(unittest.TestCase):

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
        player = Token()
        rectangle = Rectangle(80, 80, 80, 80)
        ActionTimer(20, player.remove, None)
        ActionTimer(40, rectangle.remove, None)



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
                assert 0 <= d <= 2
            if self.test_frame == QUIT_FRAME:
                self.quit()
        
        #in TESTXYZ setup:
        board.test_title = self.__class__.__name__
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


