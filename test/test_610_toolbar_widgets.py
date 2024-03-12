from miniworldmaker import App, Board, Token, Position, Toolbar, Button, Label, ToolbarLabel, loop
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test610(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board()
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                toolbar = Toolbar()
                toolbar.margin_left =  20
                toolbar.margin_right = 10
                toolbar.background_color = (255,0,255)

                button = Button("Toolbar Button")
                button.text = "Changed Text"
                button.set_image("images/arrow.png")
                button.set_border((0,0,0,255), 2)
                button.margin_bottom = 30
                toolbar.add_widget(button)

                button = Button("Toolbar Button")
                button.text = "Changed Text 2"
                button.set_image("images/arrow.png")
                button.margin_left = 10
                button.margin_right = 10
                button.set_background_color((200,200,0))
                toolbar.add_widget(button, "button 2")

                button = Label("Toolbar Label")
                button.text = "Changed Label"
                button.set_image("images/arrow.png")
                button.set_border((0,0,0,255), 2)
                button.margin_top = 30
                toolbar.add_widget(button)

                #@button.register
                #def on_clicked_left():
                #    print("clicked left")
                    
                @board.register
                def on_message(self, text):
                    print(text)

                label = ToolbarLabel("Toolbar Label")
                label.text = "Changed Label"
                label.set_image("images/arrow.png")
                label.set_border((0,0,0,255), 2)
                toolbar.add_widget(label)

                label = ToolbarLabel("Remove")
                toolbar.add_widget(label)
                toolbar.remove_widget(label)

                label = ToolbarLabel("0")
                toolbar.add_widget(label)
                label.set_image((255,0,0))
                label.padding_left = 0
                label.padding_right = 0
                label.padding_top = 0
                label.padding_bottom = 0
                label.margin_right = 10
                label.margin_left = 0
                label.img_width = 40

                label = ToolbarLabel("status")
                toolbar.add_widget(label)
                label.set_image((0,255,0))
                label.background_color = (255,255,255)
                label.padding_left = 0
                label.padding_right = 0
                label.padding_top = 0
                label.padding_bottom = 0
                label.margin_right = 0
                label.set_border((0,0,0,255), 2)
                label.text_align = "left"
                percent = 0
                @loop(frames = 10)
                def change_status():
                    nonlocal percent
                    label.img_width = label.width / 100 * percent
                    label.text = str(percent)
                    if percent < 100:
                        percent += 10
                board.add_container(toolbar, "right", size = 200)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,30,60,100,110]
        QUIT_FRAME = 110
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