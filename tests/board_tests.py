import unittest
import miniworldmaker

class TestBoard(unittest.TestCase):
    def test_board_instance(self):
        test_instance = self
        board = miniworldmaker.TiledBoard()
        board.columns=20
        board.rows=8
        board.tile_size=40
        board.fps=60
        i = 0
        @board.register
        def act(self):
            nonlocal i
            i = i + 1
            print(board.frame, i)
            if board.frame == 120:
                test_instance.assertEqual(i, 13)
                test_instance.assertEqual(board.frame, 120)
                board._app.quit()
        self.assertEqual(board.fps, 60)
        self.assertEqual(board.speed, 1)
        board.fps = 24
        self.assertEqual(board.fps, 24)
        self.assertEqual(board.speed, 1)
        board.speed=10
        self.assertEqual(board.fps, 24)
        self.assertEqual(board.speed, 10)
        with self.assertRaises(SystemExit):
            
            self.assertEqual(board.frame, 0)
            board.run()
            

if __name__ == '__main__':
    unittest.main()
    


