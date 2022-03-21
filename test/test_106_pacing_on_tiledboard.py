from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test106(unittest.TestCase):
    def setUp(self):
        board = PixelBoard(400,300)
        self.board = board
        path = os.path.dirname(__file__)
        board.app.register_path(path)
        
        @board.register
        def init_test(self):
            board.test_frame = 0
            
        
        @board.register
        def setup_environment(self, test):
            board.add_background("images/grass.jpg")
            board.columns=20
            board.rows=8
            board.tile_size=40

            player = Token(position=(3, 4))
            player.add_costume("images/char_blue.png")
            test.assertEquals(player.position, BoardPosition(3, 4))
            test.assertEquals(player.direction, 0)
            player.orientation = -90
            test.assertEquals(player.direction, 0)

        @board.register
        def on_setup(self):
            self.init_test()
    
        @board.register
        def test(self):
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

        @board.register 
        def act(self):
            self.test()
        
        #in setup
        board.test_title = self.__class__.__name__
        board.setup_environment(self)
        
        
    def test_102(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


