from miniworldmaker import *
import imgcompare
import os
import unittest
import random

TEST_FRAMES = [1,10,20,30,40,60,80,100,120]
QUIT_FRAME = 121
    
def diff(ia, ib):
    percentage = imgcompare.image_diff_percent(ia, ib)
    return percentage

class Test405(unittest.TestCase):

    def setUp(self):
        """ Programmcode here:
            You need:
            
            a) Your board must have the name `board`
            b) init_test() must be called in on_setup,
            or additionally on_setup-Method must be added
            b) An act-method, where self.test() is called
        """
        App.reset(unittest = True, file = __file__)

        # Is player 1 sensing player 2? Should return True
        board = PhysicsBoard((400, 200))
        anchors = []
        circles = []

        def add_line(obj1, obj2):
            l = Line(obj1.center, obj2.center)
            l.physics.simulation = None
            l.border = 1
            @l.register
            def act(self):
                self.start_position = obj1.center
                self.end_position = obj2.center
                
        for i in range(5):
            anchor = Token()
            anchor.size = (20,20)
            anchor.center = (i*50+50, 50)
            anchor.physics.simulation = "manual"
            anchors.append(anchor)
            
            c = Circle((0,0),10)
            circles.append(c)
            if i==0:
                c.center = (-50, 25)
                print("setup anchor:", anchor.center, anchor.local_center, anchor.topleft)
                print("setup circle:", c.center, c.local_center, c.topleft)
            else:
                c.center = anchor.center
                print("setup anchor:", anchor.center, anchor.local_center, anchor.topleft)
                print("setup circle:", c.center, c.local_center, c.topleft)
                c.y += 100
            c.physics.simulation = "simulated"
            anchor.physics.join(c)
            add_line(anchor, c)
    
    
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


