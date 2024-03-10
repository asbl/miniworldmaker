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

class Test228(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)


        board = TiledBoard(8,8)
        tile1 = board.get_tile((0,0))
        tile2 = board.get_tile((6,6))
        t = Token(5,6)
        tile3 = Tile.from_token(t)
        tile4 = board.get_tile((7,7))
        t2 = Token(7,7)
        
        print(tile1)
        print(tile2)
        print(tile1.distance_to(tile2))
        print(tile3.distance_to(tile2))
        print(tile1.distance_to(tile4))
        assert 8 < tile1.distance_to(tile2) < 8.5
        assert 0.9 < tile3.distance_to(tile2) < 1.1
        assert 9.5 < tile1.distance_to(tile4) < 10
        assert tile3.distance_to(tile4) == t.get_distance_to((7,7))
        print(t.get_distance_to(t2), tile3.distance_to(tile4))
        assert abs(t.get_distance_to(t2) - tile3.distance_to(tile4)) < 0.1

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


