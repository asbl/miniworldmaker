from miniworldmaker import App, Board, Token, Position, Toolbar, YesNoButton, Button
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test612(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(400, 200)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board = Board()

                toolbar = Toolbar()
                toolbar.margin_left =  20
                toolbar.margin_right = 10
                toolbar.background_color = (0,0,255)
                button = YesNoButton("Yes", "No")
                yes = button.get_yes_button()
                yes.background_color = (0, 255, 0)
                no = button.get_no_button()
                no.background_color = (255, 0, 0)
                toolbar.add_widget(button)
                button2 = Button("test")
                toolbar.add_widget(button2)
                board.add_container(toolbar, "right", size = 300)
                @board.register
                def on_message(self, message):
                    print(message)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 50
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        if hasattr(board, "setup_environment"):
            board.setup_environment(self)

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()