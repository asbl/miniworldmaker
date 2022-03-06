from miniworldmaker import *
import imgcompare
import os
import unittest

import sys, os


def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test101(unittest.TestCase):
    def setUp(self):
        board = TiledBoard(8,6)
        self.board = board
        path = os.path.dirname(__file__)
        print("register ", path)
        board.app.register_path(path)
        
        @board.register
        def init_test(self):
            board.test_frame = 0
            board.test_title = self.__class__.__name__
        
        @board.register
        def on_setup(self):
            self.init_test()
            self.columns = 5
            self.rows = 5
            self.tile_size = 40
            
            print("start test")
            self.add_background("images/grass.jpg")
            token = Token()
            token.position = (4,4)
            token.add_costume("images/player.png")
    
        @board.register
        def test(self):
            self.test_frame = self.test_frame + 1
            if self.test_frame == 1:
                print("Screenshot")
                path = os.path.dirname(__file__)
                file_test = path + f'/output/{self.test_title}_test.png'
                file_output = path + f"/output/{self.test_title}.png"
                if not os.path.isfile(file_test):
                    board.screenshot(file_test)
                board.screenshot(file_output)
                d = diff(file_test, file_output)
                assert 0 <= d <= 0.05
                self.quit()

        @board.register 
        def act(self):
            self.test()
    
    def test_101(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
  unittest.main()

