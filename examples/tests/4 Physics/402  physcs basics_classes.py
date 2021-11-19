import random
import miniworldmaker as mwm

class Board(mwm.PhysicsBoard):
    
    def on_setup(self):
        self.add_background((0,0,0,255))
        a = A()
        b = B()
        c = C()
        d = D()

class A(mwm.Token):
    def on_setup(self):
        self.position = (75, 200)
        self.add_costume("images/fly.png")
        self.physics.simulation = "simulated"

class B(mwm.Token):
    def on_setup(self):
        self.position = (175, 200)
        self.add_costume("images/fly.png")
        self.physics.simulation = "manual"
        
class C(mwm.Token):
    def on_setup(self):
        self.position = (275, 200)
        self.add_costume("images/fly.png")
        self.physics.simulation = "simulated"
        
class D(mwm.Token):
    def on_setup(self):
        self.position = (375, 200)
        self.add_costume("images/fly.png")
        self.physics.simulation = "static"

board = Board(600, 600)
board.run()



