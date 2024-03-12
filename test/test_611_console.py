from miniworldmaker import App, Board, Token, Position, Console, loop
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test611(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            #@TODO: Fix test
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                console = Console()
                console.newline("test")

                @loop(frames = 50)
                def newline():
                    console.newline(f"newline at frame {board.frame}")

                board.add_container(console, "bottom")

                @board.register
                def on_message(self, message):
                    print(message)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,50,100,150,200]
        QUIT_FRAME = 200
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