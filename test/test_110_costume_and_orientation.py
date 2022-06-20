from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test110(unittest.TestCase):
    
    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        import pygame

        board = Board()
        # Black board
        board.add_background((0, 0, 0, 100))
        board.size = (400, 300)
        # tokens looking:
        # * up(dir 0, or:-90)
        # * down(dir 0, or:90)
        # * left(dir 0, or:180)
        # * right(dir 0, or:270)

        # Token1 at position (2,1) with player costume
        token1 = Token(position=(0, 50))
        token1.add_costume("images/player.png")
        token1.costume.orientation = -90
        assert token1.position == Position(0, 50)
        assert token1.direction == 0
        assert token1.orientation == -90

        token2 = Token(position=(0, 100))
        token2.add_costume("images/player.png")
        token2.costume.orientation = 90
        token3 = Token(position=(0, 150))
        token3.add_costume("images/player.png")
        token3.costume.orientation = 180
        token4 = Token(position=(0, 200))
        token4.add_costume("images/player.png")
        token4.costume.orientation = 270

        assert token4.position == Position(0, 200)
        assert token4.rect == pygame.Rect(0, 200, 40, 40)

        class UpToken(Token):
            def on_setup(self):
                self.direction = 0
                self.costume.orientation = -90

        class LeftToken(Token):
            def on_setup(self):
                self.direction = -90
                self.costume.orientation = -90

        class DownToken(Token):
            def on_setup(self):
                self.direction = 180
                self.costume.orientation = -90

        class RightToken(Token):
            def on_setup(self):
                self.costume.orientation = -90
                self.direction = 90
                


        r = RightToken(position=(50, 50))
        r.add_costume("images/player.png")
        l = LeftToken(position=(50, 100))
        l.add_costume("images/player.png")
        u = UpToken(position=(50, 150))
        u.add_costume("images/player.png")
        d = DownToken(position=(50, 200))
        d.add_costume("images/player.png")


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
                assert 0 <= d <= 2
                self.quit()
        
        #in TESTXYZ setup:
        board.test_title = self.__class__.__name__
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


