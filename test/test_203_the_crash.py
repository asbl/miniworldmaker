from miniworldmaker import App, Board, Token, Position, TiledBoard
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test203(unittest.TestCase):

    def setUp(self):
        def test_code():
            class MyBoard(TiledBoard):

                def setup_environment(self, test):
                    robot1 = Robot(position=(0, 0))
                    robot1.add_costume("images/robo_green.png")
                    robot1.costume.orientation = - 90
                    robot1.direction = "right"
                    robot2 = Robot(position=(4, 0))
                    robot2.add_costume("images/robo_yellow.png")
                    robot2.costume.orientation = - 90
                    robot2.direction = "left"
                    self.add_background("images/water.png")
                    self.init_test()

            class Explosion(Token):
                def on_setup(self):
                    self.add_costume("images/explosion.png")


            class Robot(Token):

                def act(self):
                    self.move()
                    other = self.sensing_token(token_filter=Robot)
                    if other:
                        print("sensed", self, other, self.board.tokens)
                        explosion = Explosion(position=self.position)
                        print("exploded")
                        self.remove()
                        print("self.removed")
                        other.remove()
                        print("other.removed")


            board = MyBoard(5, 1)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1,2,3,4,5]
        QUIT_FRAME = 5
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

