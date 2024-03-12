from miniworldmaker import *
import imgcompare
import os
import unittest
from .screenshot_tester import ScreenshotTester

class Test107(unittest.TestCase):
    def setUp(self):
        def test_code():
            """
            Test code here

            Returns
                Board which should be used by tester
            """
            board = PixelBoard(400, 300)
            @board.register
            def setup_environment(self, test):
                board.add_background("images/stone.jpg")
                obj1 = Token(position=(50, 50))
                obj1.size = (80, 80)
                obj2 = Token(position=(140, 50))
                obj2.size = (20, 80)
                obj3 = Token(position=(170, 50))
                obj3.size = (20, 20)

                pl1 = Token(position=(50, 200))
                pl1.add_costume("images/player")
                pl1.size = (80, 80)

                pl2 = Token(position=(140, 200))
                pl2.add_costume("images/player")
                pl2.size = (20, 80)

                pl3 = Token(position=(170, 200))
                pl3.add_costume("images/player")
                pl3.size = (20, 20)

                class Sizer(Token):
                    def on_setup(self):
                        self.size = (80, 80)

                pl4 = Sizer(position=(240, 200))
                pl4.add_costume("images/player")

                class Sizer2(Token):
                    def on_setup(self):
                        self.size = (30, 30)

                pl5 = Sizer2(position=(290, 200))
                pl5.add_costume("images/player")
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

    


    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()
