from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test109(unittest.TestCase):
    
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
        # Black board
        board.add_background((0, 0, 0, 100))


        # Token1 at position (2,1) with player costume
        token1 = Token(position=(0, 0))
        token1.add_costume("images/player.png")
        token1.costume.orientation = -90
        assert token1.position == (0,0)
        assert token1.direction == 0
        assert token1.costume.orientation == - 90
        token2 = Token(position=(0, 40))
        token2.add_costume("images/player.png")
        token2.costume.orientation = 90
        token3 = Token(position=(0, 80))
        token3.add_costume("images/player.png")
        token3.costume.orientation = 180
        token4 = Token(position=(0, 120))
        token4.add_costume("images/player.png")
        token4.costume.orientation = 270


        # Unit circle
        token6 = Token(position=(120, 0))
        token6.add_costume("images/player.png")
        token6.costume.orientation = -90
        token6.direction_at_unit_circle = 0
        token7 = Token(position=(120, 40))
        token7.add_costume("images/player.png")
        token7.costume.orientation = -90
        token7.direction_at_unit_circle = 90
        token8 = Token(position=(120, 80))
        token8.add_costume("images/player.png")
        token8.costume.orientation = -90
        token8.direction_at_unit_circle = 180
        token9 = Token(position=(120, 120))
        token9.add_costume("images/player.png")
        token9.costume.orientation = -90
        token9.direction_at_unit_circle = 270

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


