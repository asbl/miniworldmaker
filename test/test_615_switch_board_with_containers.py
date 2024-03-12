from miniworldmaker import App, Board, Token, Position, PixelBoard, Console
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test615(unittest.TestCase):

    def setUp(self):
        def test_code():
            # Here comes your code
            class Board1(PixelBoard):
                def setup_environment(self, test):
                    self.add_background((0,255,0,255))
                    print("board 1 was created")
                    token = Token((10,10))
                    self.console = Console()
                    self.add_container(self.console, "bottom", size = 200)
                    
                def act_test(self):
                    if self.frame == 20:
                        print("board 1 is running", self.frame)
                        board2 = Board2((400, 600))
                        self.remove_container(self.console)
                        self.attach_board(board2)
                        self.switch_board(board2)
                        
                
            class Board2(PixelBoard):
                def on_setup(self):
                    self.add_background((0,0,100,255))
                    token = Token((40,40))
                    print("board 2 was created")  
                    
                def act(self):
                    self.test()           
            board = Board1(400,600)
            return board
        
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,41]
        QUIT_FRAME = 41
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)



        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()