from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test140(unittest.TestCase):
    
    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = Board()
        token = Token()
        token.remove_costume()
        assert token.costume_count == 0
        token.add_costume((255,0,0))
        assert token.costume_count == 1
        token.add_costume((0,255,0))
        print(token.costumes)
        assert token.costume_count == 2
        token.remove_costume()
        print(token.costumes)
        assert token.costume_count == 1
        token.remove_costume()
        assert token.costume_count == 0


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
            print("test")
            self.test_frame = self.test_frame + 1
            if self.test_frame == 1:
                print("Screenshot")
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
                self.quit()
        
        #in TESTXYZ setup:
        board.test_title = self.__class__.__name__
        
        
    def test_108(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


