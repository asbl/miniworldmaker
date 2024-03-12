from miniworldmaker import App, TiledBoard, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test1913(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = TiledBoard(10,4)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                def create_token(x, y):
                    t = Token()
                    t.position = (x, y)
                    t.add_costume("images/alien1.png")
                    t.border = 1
                    return t

                t0 = create_token(0,0)
                print(t0.size)
                print(t0.costume.is_upscaled)
                print(t0.costume.is_scaled)
                print(t0.costume.is_scaled_to_width)
                print(t0.costume.is_scaled_to_height)

                t0b = create_token(1,0)

                t = create_token(2,0)
                t.costume.is_scaled = True

                t = create_token(3,0)
                t.costume.is_scaled_to_width = True

                t = create_token(4,0)
                t.costume.is_scaled_to_height = True

                t = create_token(5,0)
                t.costume.is_textured = True

                t = create_token(6,0)
                t.costume.is_textured = True
                t.costume.texture_size = (10,10)

                t = create_token(7,0)
                t.flip_x()

                t = create_token(8,0)
                t.is_rotatable = False
                t.flip_x()


                # ----------------- row 2

                t = create_token(0,1)

                t = create_token(1,1)
                t.orientation = -90

                t = create_token(2,1)
                t.orientation = -180

                t = create_token(3,1)
                t.orientation = -270
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
