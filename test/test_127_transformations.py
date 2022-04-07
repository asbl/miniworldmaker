from miniworldmaker import *
import imgcompare
import os
import unittest

TEST_FRAMES = [1]
QUIT_FRAME = 1
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test127(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = Board(800,400)

        def create_token(x, y):
          t = Token()
          t.position = (x, y)
          t.add_costume("images/alien1.png")
          t.border = 1
          return t

        def create_player(x, y):
          t = Token()
          t.position = (x, y)
          t.add_costume("images/player.png")
          t.border = 1
          return t

        t0 = create_token(0,0)
        print(t0.size)
        print(t0.costume.is_upscaled)
        print(t0.costume.is_scaled)
        print(t0.costume.is_scaled_to_width)
        print(t0.costume.is_scaled_to_height)

        t0b = create_token(40,0)
        t0b.size=(80,80)

        t = create_token(120,0)
        t.size=(80,80)
        t.costume.is_scaled = True

        t = create_token(200,0)
        t.size=(80,80)
        t.costume.is_scaled_to_width = True

        t = create_token(280,0)
        t.size=(80,80)
        t.costume.is_scaled_to_height = True

        t = create_token(360,0)
        t.size=(80,80)
        t.costume.is_textured = True

        t = create_token(440,0)
        t.size=(80,80)
        t.costume.is_textured = True
        t.costume.texture_size = (10,10)

        t = create_token(520,0)
        t.size=(80,80)
        t.flip_x()

        t = create_token(600,0)
        t.is_rotatable = False
        t.size=(80,80)
        t.flip_x()


        # ----------------- row 2

        t = create_token(0,90)
        t.size=(80,80)

        t = create_token(80,90)
        t.orientation = -90
        t.size=(80,80)

        t = create_token(160,90)
        t.orientation = -180
        t.size=(80,80)

        t = create_token(240,90)
        t.orientation = -270
        t.size=(80,80)

        t = create_token(240,90)
        t.orientation = -270
        t.size=(80,80)


        t = create_token(320,90)
        t.direction = 90
        t.size=(80,80)


        t = create_token(400,90)
        t.orientation = 180
        t.size=(80,80)


        t = create_token(480,90)
        t.orientation = 270
        t.size=(80,80)

        t = create_token(560,90)
        t.orientation = 45
        t.size=(80,80)

        #-- row 3

        t = create_player(0,180)
        t.size=(80,80)

        t = create_player(80,180)
        t.costume.is_upscaled = True
        t.size=(80,80)

        t = create_player(160,180)
        t.costume.is_scaled = True
        t.size=(80,80)


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


