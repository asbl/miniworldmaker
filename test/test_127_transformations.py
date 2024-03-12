from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test127(unittest.TestCase):

    def setUp(self):
        App.reset(unittest=True, file=__file__)
        board = self.test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_code(self):
        board = Board(800, 400)

        # Here comes your code
        @board.register
        def setup_environment(self, test):
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

            t0 = create_token(0, 0)

            t0b = create_token(40, 0)
            t0b.size = (80, 80)

            t = create_token(120, 0)
            t.size = (80, 80)
            t.costume.is_scaled = True

            t = create_token(200, 0)
            t.size = (80, 80)
            t.costume.is_scaled_to_width = True

            t = create_token(280, 0)
            t.size = (80, 80)
            t.costume.is_scaled_to_height = True

            t = create_token(360, 0)
            t.size = (80, 80)
            t.costume.is_textured = True

            t = create_token(440, 0)
            t.size = (80, 80)
            t.costume.is_textured = True
            t.costume.texture_size = (10, 10)

            t = create_token(520, 0)
            t.size = (80, 80)
            t.flip_x()

            t = create_token(600, 0)
            t.is_rotatable = False
            t.size = (80, 80)
            t.flip_x()

            # ----------------- row 2

            t = create_token(0, 90)
            t.size = (80, 80)

            t = create_token(80, 90)
            t.orientation = -90
            t.size = (80, 80)

            t = create_token(160, 90)
            t.orientation = -180
            t.size = (80, 80)

            t = create_token(240, 90)
            t.orientation = -270
            t.size = (80, 80)

            t = create_token(240, 90)
            t.orientation = -270
            t.size = (80, 80)

            t = create_token(320, 90)
            t.direction = 90
            t.size = (80, 80)

            t = create_token(400, 90)
            t.orientation = 180
            t.size = (80, 80)

            t = create_token(480, 90)
            t.orientation = 270
            t.size = (80, 80)

            t = create_token(560, 90)
            t.orientation = 45
            t.size = (80, 80)

            # -- row 3

            t = create_player(0, 180)
            t.size = (80, 80)

            t = create_player(80, 180)
            t.costume.is_upscaled = True
            t.size = (80, 80)

            t = create_player(160, 180)
            t.costume.is_scaled = True
            t.size = (80, 80)

        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()
