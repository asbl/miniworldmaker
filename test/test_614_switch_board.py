from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test614(unittest.TestCase):

    def setUp(self):
        def test_code():
            class Board1(PixelBoard):
                def setup_environment(self, test):
                    self.rows = 100
                    self.columns = 100
                    self.add_background((0,0,100,255))
                    print("board 1 was created")
                    self.token = Token((10,10))
                    self.token.color = (255, 0, 0)
                    self.token.direction = "right"
                    print(self.event_manager.registered_events)
                    
                def act_test(self):
                    print("act", self.frame)
                    if self.frame < 30:
                        self.token.move()
                    elif self.frame == 30:
                        print("switch to board 2", self.frame)
                        board2 = Board2((400, 600))
                        self.attach_board(board2)
                        self.switch_board(board2)
                        
                
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
                    
                def act(self):
                    self.test()
                    if self.frame > 80:
                        self.token.move()
                        print("token rect", self.token.get_local_rect())
                    

            board = Board1(400,600)
            return board
                
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,41, 81, 101]
        QUIT_FRAME = 101
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)



        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()

