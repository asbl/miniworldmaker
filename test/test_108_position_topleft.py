from miniworldmaker import *
import imgcompare
import os
import unittest

def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test108(unittest.TestCase):
    
    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        board = PixelBoard(400, 400)
        board.add_background((100, 0, 0, 255))

        a = Token()
        a.position = (0,0)
        assert a.topleft == (0,0)
        b = Token()
        b.topleft = (100,100)
        assert b.topleft == (100, 100)
        assert b.position == (100.0, 100.0)
        c = Token()
        c.position = (200,200)
        assert c.topleft == (200.0, 200.0)
        assert c.position == (200, 200)
        assert c.center == (220, 220)
        assert c.x == 200
        assert c.y == 200
        d = Token()
        d.center = (250,250)
        
        assert d.topleft == (230, 230)
        assert d.position == (230, 230)
        assert d.center == (250, 250)
        path = os.path.dirname(__file__)
        board.app.register_path(path)

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


