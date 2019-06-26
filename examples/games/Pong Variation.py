from miniworldmaker import *

class MyBoard(ProcessingBoard):
    

    
    
    def on_setup(self):
        self.fill((0,0,0, 255))
        self.circle = Circle((20,100), 10, 0, color=(255,255,255,255))
        self.circle.physics.elasticity = 0.95
        self.circle.start_physics()
        self.rectangle1 = Rectangle((5,200), 10, 100, 10, color = (255,255,255,255))
        self.rectangle1.physics.elasticity = 1.22
        self.rectangle1.physics.gravity = False
        self.rectangle1.start_physics()
        self.rectangle2 = Rectangle ((785, 250), 10, 100, 10, color = (255,255,255,255))
        self.rectangle2.physics.elasticity = 1.22
        self.rectangle2.physics.gravity = False
        self.rectangle2.start_physics()
        self.line = Line ((0,500), (100,600), 10, color = (255,255,255,255))
        self.line.physics.elasticity = 1
        self.line.start_physics()
        self.line = Line ((800,500), (700,600), 10, color = (255,255,255,255))
        self.line.physics.elasticity = 1
        self.line.start_physics()
        self.line = Line ((0,100), (100,0), 10, color = (255,255,255,255))
        self.line.physics.elasticity = 1
        self.line.start_physics()
        self.line = Line ((700,0), (800,100), 10, color = (255,255,255,255))
        self.line.physics.elasticity = 1
        self.line.start_physics()
        self.down = True
        self.circle.l_pos=self.circle.position

    def act(self):
        print(self.circle.last_position.x)
        print("start", self.circle.l_pos.x)
        print("start", self.circle.position.x)
        self.speed_x =  self.circle.position.x - self.circle.l_pos.x
        if self.rectangle1.y < 400 and self.down:
            self.rectangle1.y += 2
            #self.rectangle2.y += 2
        else:
            pass
        print("middle", self.circle.l_pos.x)
        print("middle", self.circle.position.x)
        self.circle.last_position = self.circle.position
        print("end", self.circle.l_pos.x)
        print("end", self.circle.position.x)
        self.circle.l_pos = self.circle.position
        
    
        
   
    
    
    def on_key_pressed(self, keys):
        if "SPACE" in keys:    
            self.circle.physics.velocity_y = 370
    
myboard = MyBoard(800, 600)
myboard.show()