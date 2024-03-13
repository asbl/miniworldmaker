from miniworldmaker import App, Board, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os


class Test102(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = Board(200, 400)
            path = os.path.dirname(__file__)
            board.app.register_path(path)
            board.tile_size = 40
            board.add_background("images/grass.png")
            token = Token()
            token.position = (4, 4)
            token.add_costume("images/player.png")

            # Token 1: Purple in topleft corner
            token1 = Token(position=(0, 0))
            token1.size = (40, 40)  # should be in topleft corner
            assert token1.position, (0, 0)

            token2 = Token(position=(40, 40))
            assert token2.position, Position(40, 40)
            token2.size = (40, 40)
            assert token2.position, Position(40, 40)
            assert token2.size, (40, 40)

            # Token 3: Below token1, created with Image "1"
            token3 = Token(position=(40, 80))
            token3.add_costume("images/1.png")
            token3.size = (40, 40)
            assert token3.position, Position(40, 80)

            # Token 4: Below token1, created with Image "2" in `on_setup`-Method
            class MyToken(Token):
                def on_setup(self):
                    self.add_costume("images/2.png")

            token4 = MyToken(position=(40, 130))
            assert token4.position, Position(40, 130)

            # Token5: Created with image "3" without file ending
            token5 = Token(position=(60, 200))
            token5.add_costume("images/3")
            assert token5.position == Position(60, 200)
            # assert token5.costume.image.get_width() == 40
            # assert token5.costume.image.get_height() == 40

            # Token6: Created with images "1" and "2", switches from
            class SwitchBackground(Token):
                def on_setup(self):
                    self.add_costume("images/1")
                    self.add_costume("images/2")

            SwitchBackground(position=(60, 250))

            # Token 7: Like 6, but switches to costume 1 (remember, counting from 0)
            token7 = SwitchBackground(position=(67, 307))
            token7.switch_costume(1)

            # Token 7 throws error because switching to costume 2 is not allowed
            with self.assertRaises(CostumeOutOfBoundsError):
                token7.switch_costume(2)

            # Token 8: Purple in topleft corner (with center)
            token8 = Token()
            token8.size = (40, 40)
            token8.center = (200, 0)
            return board
        App.reset(unittest=True, file=__file__)
        board = test_code()
        """ Setup screenshot tester"""
        TEST_FRAMES = [1]
        QUIT_FRAME = 1
        tester = ScreenshotTester(TEST_FRAMES, QUIT_FRAME, self)
        tester.setup(board)
        

    def test_main(self):
        with self.assertRaises(SystemExit):
            self.board.run()


if __name__ == "__main__":
    unittest.main()
