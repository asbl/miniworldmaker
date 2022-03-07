from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test103(unittest.TestCase):
    def setUp(self):
        board = Board(8,6)
        self.board = board
        path = os.path.dirname(__file__)
        print("register ", path)
        board.app.register_path(path)
        
        @board.register
        def init_test(self):
            board.test_frame = 0
            
        
        @board.register
        def setup_environment(self, test):
            board = TiledBoard()
            # Black board
            board.add_background((0, 0, 0, 100))
            board.columns = 5
            board.rows = 5
            board.tile_size = 40

            # Token1 at position (2,1) with player costume
            token1 = Token(position=(2, 1))
            token1.add_costume("images/player.png")
            # Token2 at position (3,1) with purple backgrund
            token2 = Token(position = (3, 1) )
            token2.add_costume((100,0,100,100))
            with test.assertRaises(SizeOnTiledBoardError):
                token2.size = (1,1)
            token2.posisition = (40,40)
                        
        @board.register
        def on_setup(self):
            self.init_test()
    
        @board.register
        def test(self):
            self.test_frame = self.test_frame + 1
            if self.test_frame == 1:
                print("Screenshot")
                path = os.path.dirname(__file__)
                if path:
                    path = "/" + path
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


