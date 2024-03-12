from miniworldmaker import App, HexBoard, CubeCoord, HexEdge, HexCorner, HexTile, Token, Position, CostumeOutOfBoundsError
from .screenshot_tester import ScreenshotTester
import unittest
import os
import random


class Test2001(unittest.TestCase):

    def setUp(self):
        def test_code():
            board = HexBoard(12, 12)
            # Here comes your code
            @board.register
            def setup_environment(self, test):
                board.tile_size = 40
                for x in range(board.columns):
                    for y in range(board.rows):
                        t = Token((x,y))
                        t.add_costume(f"images/grass_08.png")
                        t.static = True

                token = Token((0,1)) # move right to (1,0)
                token.size = 1
                token.inner = True
                #token.add_costume("images/castle_large.png")

                token = Token((1,1)) # move right to (1,0)
                token.size = 1
                token.fill_color = (255,0,0,100)
                token.inner = True

                token = Token((0,3))

                #token.add_costume("images/castle_large.png")
                token.size = 0.1
                token.fill_color=(0,0,0)
                token.corner = "n"

                print("# BORDERS")
                c1 = board.get_corner_from_tile((2,0),"sw")
                c2 = board.get_corner_from_tile((2,1),"n")
                # (2,0).sw and (2.1).n are the same coordinates!
                assert(c1.position == CubeCoord(3,1,-2))
                assert(c1.direction == CubeCoord(1,1,0))
                assert(c2.position == CubeCoord(3,1,-2))
                assert(c2.direction == CubeCoord(1,1,0))
                assert(c1 == c2)
                # Edge

                edge = HexEdge.from_tile((0,5), "nw")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (10,10,10,100)
                token.direction = edge.get_direction()
                print("First edge", edge, edge.position, token, token.position)

                edge = HexEdge.from_tile((0,5), "w")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (40,40,40,100)
                token.direction = edge.get_direction()

                edge = HexEdge.from_tile((0,5), "sw")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (90,90,90,100)
                token.direction = edge.get_direction()

                edge = HexEdge.from_tile((0,5), "so")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (140,140,140,100)
                token.direction = edge.get_direction()

                edge = HexEdge.from_tile((0,5), "o")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (180,180,180,100)
                token.direction = edge.get_direction()

                edge = HexEdge.from_tile((0,5), "no")
                token = Token()
                token.center = edge.position
                token.size = (0.2, 0.4)
                token.color = (220,220,220,100)
                token.direction = edge.get_direction()

                """
                # CORNERS
                """
                corner = HexCorner.from_tile((2,3), "no")
                token = Token()
                token.center = corner.position

                token.size = (0.2, 0.2)
                token.fill_color = (40,40,40,100)

                corner = HexCorner.from_tile((2,3), "so")
                token = Token()
                token.center = corner.position
                token.size = (0.2, 0.2)
                token.fill_color = (120,120,120,255)

                corner = HexCorner.from_tile((2,3), "s")
                token = Token()
                token.center = corner.position
                token.size = (0.2, 0.2)
                token.fill_color = (140,140,140,255)

                corner = HexCorner.from_tile((2,3), "sw")
                token = Token()
                token.center = corner.position
                token.size = (0.2, 0.2)
                token.fill_color = (170,170,170,255)

                corner = HexCorner.from_tile((2,3), "nw")
                token = Token()
                token.center = corner.position
                token.size = (0.2, 0.2)
                token.fill_color = (200,200,200,255)

                corner = HexCorner.from_tile((2,3), "n")
                token = Token()
                token.center = corner.position
                token.fill_color = (255,255,255)
                token.size = (0.2, 0.2)
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
