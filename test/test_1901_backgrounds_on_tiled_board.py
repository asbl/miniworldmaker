from miniworldmaker import App, TiledBoard, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1901(unittest.TestCase):

    def setUp(self):
        def test_code():
            # Here comes your code
            class MyBoard(TiledBoard):
                def setup_environment(self, test):
                    self.init_test()            
                    path = os.path.dirname(__file__)
                    board.app.register_path(path)
                    self.columns = 5
                    self.rows = 5
                    self.tile_size = 40
                    self.add_background("images/stone.png")
                    print(self.background)
                    token = Token()
                    token.position = (3,4)
                    assert(token.costume.is_rotatable == True)
                    assert(type(token.position) == Position)
                    print(token, token.costumes)
                    print("costume:", token.costume)
                    print(token.costume.images)
                    token.add_costume("images/player.png")
                    print(token.costumes)
                    
                    print(token.costume.images)
                    assert(token.costume.is_upscaled == True)
                    # Bilder von:
                    # https://www.kenney.nl/assets
                        
            board = MyBoard()
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
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