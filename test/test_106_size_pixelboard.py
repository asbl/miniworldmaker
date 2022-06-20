from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test106_1(unittest.TestCase):
    def setUp(self):
        board = PixelBoard(400,300)
        path = os.path.dirname(__file__)
        board.app.register_path(path)
        self.board = board
        path = os.path.dirname(__file__)
        board.app.register_path(path)
        
        @board.register
        def init_test(self):
            board.test_frame = 0
            
        
        @board.register
        def setup_environment(self, test):
            board.add_background("images/stone.jpg")

            obj1 = Token(position=(50, 50))
            obj1.size = (80,80)
            obj2 = Token(position=(140, 50))
            obj2.size = (20,80)
            obj3 = Token(position=(170, 50))
            obj3.size = (20,20)

            pl1 = Token(position=(50, 200))
            pl1.add_costume("images/player")
            pl1.size = (80, 80)

            pl2 = Token(position=(140, 200))
            pl2.add_costume("images/player")
            pl2.size = (20, 80)

            pl3 = Token(position=(170, 200))
            pl3.add_costume("images/player")
            pl3.size = (20, 20)

            class Sizer(Token):
                def on_setup(self):
                    self.size = (80,80)
                    
            pl4 = Sizer(position=(240, 200))
            pl4.add_costume("images/player")

            class Sizer2(Token):
                def on_setup(self):
                    self.size = (30,30)
              
            pl5 = Sizer2(position=(290, 200))
            pl5.add_costume("images/player")


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
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


