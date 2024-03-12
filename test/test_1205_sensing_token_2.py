from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1205(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                
                wall=Token((200,0))
                wall.color = (255,255,255)
                wall.size = (20, 400)

                for i in range(7):
                    token = Token((10,i*60))
                    token.color = (255,255,255)
                    token.range = i * 10
                    token.number = i % 4
                    @token.register
                    def act(self):
                        if self.number == 0:
                            if not self.sensing_token(wall):
                                self.direction = "right"
                                self.move()
                        if self.number == 1:
                            if not self.sensing_token():
                                self.direction = "right"
                                self.move()
                        if self.number == 2:
                            if not self.sensing_tokens():
                                self.direction = "right"
                                self.move()
                        if self.number == 3:
                            if not self.sensing_tokens(wall):
                                self.direction = "right"
                                self.move()
            return board
                        
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,20,40,60,80,120,140,150,170]
        QUIT_FRAME = 170
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
