from miniworldmaker import *
import imgcompare
import os
import sys
import unittest

TEST_FRAMES = [1,41, 81, 101]
QUIT_FRAME = 101
TEST_TITLE = "Test614"
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test1401(unittest.TestCase):
    
    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)
        
        class Test:
            
            running_test = None
            
            def __init__(self, parent):
                self.parent = parent
                Test.running_test = self
                
            def setup(self, board):
                global TEST_TITLE
                self.board = board
                self.test_frame = 0
                self.test_title = TEST_TITLE
                print("setup test")
                
            @classmethod
            def from_running(cls):
                return cls.running_test
        
            def process_test(self):
                global TEST_FRAMES
                global QUIT_FRAME
                print(self.test_frame)
                self.test_frame = self.test_frame + 1
                if self.test_frame in TEST_FRAMES:
                    print("screenshot test at frame",  self.test_frame)
                    path = os.path.dirname(__file__)
                    if path != "":
                        path =  path + "/"
                    file_test = path + f'output/{self.test_title}_test_{self.test_frame}.png'
                    file_output = path + f"output/{self.test_title}_{self.test_frame}.png"
                    if not os.path.isfile(file_test):
                        self.board.screenshot(file_test)
                    self.board.screenshot(file_output)
                    d = diff(file_test, file_output)
                    assert 0 <= d <= 0.05
                if self.test_frame == QUIT_FRAME:
                       self.board.app._unittest = True
                       self.board.quit()

        test = Test(self)
        
        """
        Here starts the program code
        """
        
        class Board1(PixelBoard):
            def on_setup(self):
                self.rows = 100
                self.columns = 100
                self.add_background((0,0,100,255))
                print("board 1 was created")
                self.token = Token((10,10))
                self.token.color = (255, 0, 0)
                self.token.direction = "right"
                self.test = test.from_running()
                self.test.setup(self)
                
            def act(self):
                if self.frame < 60:
                    self.token.move()
                else:
                    print("board 1 is running", self.frame)
                    board2 = Board2((400, 600))
                    self.switch_board(board2)
                self.test.process_test()
                    
            
        class Board2(PixelBoard):
            def on_setup(self):
                self.add_background((255,255,255,255))
                self.token = Token((80,80))
                self.token.color = (0,255,0)
                #self.token.add_costume("1.png")
                #print(self.token.costume, self.token.costume.image)
                self.token.costume.set_dirty("all", 2)
                self.token.dirty = 1
                print("token created at", self.token.get_local_rect())
                print("board 2 was created")
                print(self.app.container_manager.containers)
                self.test = Test.from_running()
                
            def act(self):
                if self.frame > 80:
                    self.token.move()
                    print("token rect", self.token.get_local_rect())
                self.test.process_test()
                
                
                
        board = Board1(400,600)
        board.run()
         
        
        """ end of setUp - code up here""" 
        
        self.board = board
        
        
    def test_main(self):
        self.board.run()
        
if __name__ == '__main__':
    unittest.main()


