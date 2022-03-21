from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test102(unittest.TestCase):
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
            self.columns = 5
            self.rows = 5
            self.tile_size = 40
            self.add_background("images/grass.jpg")
            token = Token()
            token.position = (4,4)
            token.add_costume("images/player.png")
            
            # Token 1: Purple in topleft corner
            token1 = Token(position=(0, 0))
            token1.size = (40, 40) # should be in topleft corner
            test.assertEqual(token1.position,(0,0))
            
            token2 = Token(position=(40, 40))
            test.assertEqual(token2.position,BoardPosition(40, 40))
            token2.size = (40, 40)
            test.assertEqual(token2.position, BoardPosition(40, 40))
            test.assertEqual(token2.size,(40,40))
            
            # Token 3: Below token1, created with Image "1"
            token3 = Token(position=(40, 80))
            token3.add_costume("images/1.png")
            token3.size = (40, 40)
            test.assertEqual(token3.position, BoardPosition(40, 80))

            # Token 4: Below token1, created with Image "2" in `on_setup`-Method
            class MyToken(Token):
                def on_setup(self):
                    self.add_costume("images/2.png")

            token4 = MyToken(position = (40,130))
            test.assertEqual(token4.position, BoardPosition(40, 130))

            # Token5: Created with image "3" without file ending
            token5 = Token(position=(60, 200))
            token5.add_costume("images/3")
            test.assertEqual(token5.position, BoardPosition(60, 200))
            test.assertEqual(token5.costume.image.get_width(), 40)
            test.assertEqual(token5.costume.image.get_height(), 40)

            # Token6: Created with images "1" and "2", siwtches from 
            class SwitchBackground(Token):
                def on_setup(self):
                    self.add_costume("images/1")
                    self.add_costume("images/2")
                          
            token6 = SwitchBackground(position = (60,250))

            # Token 7: Like 6, but switches to costume 1 (remember, counting from 0)
            token7 = SwitchBackground(position = (67,307))
            token7.switch_costume(1)

            # Token 7 throws error because switching to costume 2 is not allowd
            with test.assertRaises(CostumeOutOfBoundsError):
                token7.switch_costume(2)
            
            # Token 8: Purple in topleft corner (with center)
            token8 = Token()
            token8.size = (40,40)
            token8.center=(200,0)
                        
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
                    path = path + "/"
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



