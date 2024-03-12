from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test158(unittest.TestCase):

    def setUp(self):
        def test_code():
            WIDTH, HEIGHT = 800, 400
            board = Board(WIDTH, HEIGHT)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                nonlocal WIDTH, HEIGHT
                left, bottom = WIDTH/2, HEIGHT/2
                BACKGROUND = "desertback"
                back0 = Token()
                back0.add_costume(BACKGROUND)
                back0.size = WIDTH, HEIGHT
                back1 = Token(WIDTH, 0)
                back1.size = WIDTH, HEIGHT
                back1.add_costume(BACKGROUND)
                backs = [back0, back1]

                walker = Token((100, HEIGHT - 100))
                walker.size = 100, 60
                walker.add_costumes(["walk1", "walk2"])
                walker.speed = 1
                walker.count = 0

                @board.register
                def act_test(self):
                    for back in backs:
                        back.x -= 1
                        if back.x <= - WIDTH:
                            back.x = WIDTH
                    walker.count += walker.speed
                    if walker.count > 11:
                        costume = walker.next_costume()
                        walker.count = 0
                
                @board.register
                def on_key_down(self, keys):
                    if "q" in keys:
                        board.quit
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1, 5, 10, 20]
        QUIT_FRAME = 100
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)



        return board

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()