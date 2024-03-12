from miniworldmaker import App, Board, Token, Position, PixelBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test614(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
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
                        print(self.event_manager.registered_events)
                        
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

