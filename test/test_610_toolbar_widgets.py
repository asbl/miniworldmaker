from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,30,60,100,110]
QUIT_FRAME = 110
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test610(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """

        board = Board()

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
        label.img_width = 80

        label = ToolbarLabel("status")
        toolbar.add_widget(label)
        label.set_image((0,255,0))
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

        board.add_container(toolbar, "right")



        """ here act and init - delete if used in testcode"""
        
        @board.register
        def on_setup(self):
            self.init_test()            
            
        @board.register
        def act(self):
            self.test()
            
        """ end of setUp - code up here""" 
        
        self.board = board
           
        @board.register
        def init_test(self):
            print("setup test")
            board.test_frame = 0
        
        @board.register
        def test(self):
            global TEST_FRAMES
            global QUIT_FRAME
            
            self.test_frame = self.test_frame + 1
            if self.test_frame in TEST_FRAMES:
                print("screenshot test at frame",  self.test_frame)
                path = os.path.dirname(__file__)
                if path != "":
                    path =  path + "/"
                file_test = path + f'output/{self.test_title}_test_{self.test_frame}.png'
                file_output = path + f"output/{self.test_title}_{self.test_frame}.png"
                if not os.path.isfile(file_test):
                    board.screenshot(file_test)
                board.screenshot(file_output)
                d = diff(file_test, file_output)
                assert 0 <= d <= 0.05
            if self.test_frame == QUIT_FRAME:
                self.quit()
        
        #in TESTXYZ setup:
        board.test_title = self.__class__.__name__
        
        
    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()
        
if __name__ == '__main__':
    unittest.main()


