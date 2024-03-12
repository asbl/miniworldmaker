import imgcompare
import os


class ScreenshotTester:
    def __init__(self, test_frames, quit_frame, unittest):
        self.test_frames = test_frames
        self.quit_frame = quit_frame
        self.unittest = unittest
        self.test_frame = 0
        self.board = None  # Set in setup

    def setup(self, board):
        self.board = board
        self.board.test_title = self.unittest.__class__.__name__
        self.board.tester = self

        @board.register
        def on_setup(self):
            self.init_test()

        @board.register
        def act(self):
            self.test()
            if hasattr(self, "act_test"):
                self.act_test()

        self.unittest.board = board

        @board.register
        def init_test(self):
            board.test_frame = 0

        @board.register
        def test(self):
            self.tester.test_frame = self.tester.test_frame + 1
            self.tester.screenshot_test(
                self.tester.test_frame,
                self.tester.quit_frame,
                self.tester.test_frames,
                self.test_title,
                self.tester,
            )
            
        @board.register
        def attach_board(self, board2):
            board2.tester = self.tester
            board2.test_title = self.test_title
            
            @board2.register
            def test(self):
                self.tester.test_frame = self.tester.test_frame + 1
                self.tester.screenshot_test(
                    self.tester.test_frame,
                    self.tester.quit_frame,
                    self.tester.test_frames,
                    self.test_title,
                    self.tester,
                )

    def diff(self, ia, ib):
        percentage = imgcompare.image_diff_percent(ia, ib)
        return percentage

    def compare_files(self, file_test, file_output):
        d = self.diff(file_test, file_output)
        assert 0 <= d <= 0.05

    def screenshot(self, frame, test_frames, test_title):
        if not frame in test_frames:
            return False
        path = os.path.dirname(__file__)
        if path != "":
            path = path + "/"
        file_test = path + f"testfiles/{test_title}_testfile_{frame}.png"
        file_output = path + f"outputfiles/{test_title}_tmp_outputfile{frame}.png"
        print("screenshot test at frame", frame, file_output)
        if not os.path.isfile(file_test):
            self.board.screenshot(file_test)
            print("created new testimage")
        self.board.screenshot(file_output)
        return file_test, file_output

    def check_quit(
        self,
        frame,
    ):
        print("FRAME, frame, self.quit_frame", frame, self.quit_frame)
        if frame == self.quit_frame:
            self.board.quit()

    def screenshot_test(self, frame, quit_frame, test_frames, test_title, test):
        files = self.screenshot(frame, test_frames, test_title)
        if not files:
            self.check_quit(frame)
        else:
            file_test = files[0]
            file_output = files[1]
            self.compare_files(file_test, file_output)
            self.check_quit(frame)
