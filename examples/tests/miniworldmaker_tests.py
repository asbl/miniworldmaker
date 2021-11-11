import unittest
import miniworldmaker
import cv2
import sys

class TestBoard(unittest.TestCase):
    def test_speed_and_fps(self):
        """
        Set and test fps and speed
        """
        print("test_speed_and_fps")
        test_instance = self
        board = miniworldmaker.TiledBoard()
        board.columns = 20
        board.rows = 8
        board.tile_size = 40
        board.fps = 60
        i = 0
        @board.register
        def act(self):
            nonlocal i
            i = i + 1
            print(board.frame, i)
            if board.frame == 120:
                test_instance.assertEqual(i, 13)
                test_instance.assertEqual(board.frame, 120)
                board.quit()
        self.assertEqual(board.fps, 60)
        self.assertEqual(board.speed, 1)
        board.fps = 24
        self.assertEqual(board.fps, 24)
        self.assertEqual(board.speed, 1)
        board.speed=10
        self.assertEqual(board.fps, 24)
        self.assertEqual(board.speed, 10)
        self.assertEqual(board.frame, 0)
        with self.assertRaises(SystemExit):
            board.run()
        #except SystemExit:
        #    sys.exit(1)
    
    def is_image_duplicate_of(image, duplicate):
            original = cv2.imread(image)
            duplicate = cv2.imread(duplicate)
            if original.shape == duplicate.shape:
                difference = cv2.subtract(original, duplicate)
            else:
                return False
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                return True
            else:
                return False
    
    def test_costume_load(self):
        """
        Tests if backgrounds and costumes are loaded
        """
        import miniworldmaker
        print("test_costume_load")
        board = miniworldmaker.PixelBoard(400,300)
        board.add_background("images/stone.jpg")
        robot = miniworldmaker.Token(position=(50, 50))
        @miniworldmaker.timer(frames = 5)
        def screenshot():
            board.screenshot("screenshot")
            self.assertEqual(True, TestBoard.is_image_duplicate_of("screenshot.jpg","test1.jpg"))
            board.quit()
        with self.assertRaises(SystemExit):
            board.run()


if __name__ == '__main__':
    unittest.main()
    


