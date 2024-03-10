from miniworldmaker import *
import imgcompare
import os
import unittest
import random
from helper import diff

TEST_FRAMES = [1]
QUIT_FRAME = 1

class Test102(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)
        
        board = Board(200,400)
        path = os.path.dirname(__file__)
        board.app.register_path(path)
        board.tile_size = 40
        board.add_background("images/grass.png")
        token = Token()
        token.position = (4,4)
        token.add_costume("images/player.png")

        # Token 1: Purple in topleft corner
        token1 = Token(position=(0, 0))
        token1.size = (40, 40) # should be in topleft corner
        assert token1.position,(0,0)

        token2 = Token(position=(40, 40))
        assert token2.position,Position(40, 40)
        token2.size = (40, 40)
        assert token2.position, Position(40, 40)
        assert token2.size,(40,40)

        # Token 3: Below token1, created with Image "1"
        token3 = Token(position=(40, 80))
        token3.add_costume("images/1.png")
        token3.size = (40, 40)
        assert token3.position, Position(40, 80)

        # Token 4: Below token1, created with Image "2" in `on_setup`-Method
        class MyToken(Token):
            def on_setup(self):
                self.add_costume("images/2.png")

        token4 = MyToken(position = (40,130))
        assert token4.position, Position(40, 130)

        # Token5: Created with image "3" without file ending
        token5 = Token(position=(60, 200))
        token5.add_costume("images/3")
        assert token5.position == Position(60, 200)
        #assert token5.costume.image.get_width() == 40
        #assert token5.costume.image.get_height() == 40

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
        with self.assertRaises(CostumeOutOfBoundsError):
            token7.switch_costume(2)

        # Token 8: Purple in topleft corner (with center)
        token8 = Token()
        token8.size = (40,40)
        token8.center=(200,0)
        print(token8.position, token8.center)
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



