import random
import miniworldmaker as mwm

board = mwm.PhysicsBoard(800, 600)
board.game_over = False
board.add_background("images/background.png")
pipes = []

pipes.append(mwm.Token(position=(300, board.height - 280)))
pipes.append(mwm.Token(position=(500, 0)))
pipes.append(mwm.Token(position=(700, board.height - 280)))
pipes.append(mwm.Token(position=(900, 0)))

for pipe in pipes:
    pipe.direction = 0
    pipe.add_costume("images/pipe1.png")
    pipe.costume.orientation = 0
    pipe.size = (50, 280)
    pipe.passed = False
    pipe.physics.simulation = "manual"
    pipe.physics.velocity_x = -150
    
    @pipe.register
    def act(self):
        print(pipe.physics._body.position)
        
#self.move_in_direction("left")
#self.direction = 0
#        if self.position.x < 75 and self.passed is False:
#            self.passed = True
#            score.inc()
            
    @pipe.register
    def on_sensing_left_border(self):
        position = (self.center_x + random.randint(750, 800), self.center_y)
        self.move_to(position)
        self.passed = False

pipes[1].costume.orientation = -180
pipes[3].costume.orientation = -180

score = mwm.NumberToken()
score.physics.simulation = "static"
score.position = (30, 30)
score.size = (40, 40)
score.physics.simulation = "static"
board.stop()
bird = mwm.Token()
bird.position = (75, 200)
bird.add_costume("images/fly.png")
bird.size = (60, 60)
bird.physics.simulation = "simulated"
bird.is_flipped = True
bird.physics.size = (0.8, 0.8)
bird.physics.shape_type = "circle"
#bird.costume.orientation = 90
#bird.flip_x()
bird.is_rotatable = False

@bird.register
def on_sensing_borders(self, borders):
    if "bottom" in borders or "top" in borders:
        end=mwm.TextToken()
        end.set_text("Game over!")
        end.position = (400,200)
        board.game_over = True
        board.stop()

@bird.register
def on_touching_token(self, other, info):
    print("I'm touching something")
    #end=mwm.TextToken()
    #end.set_text("Game over!")
    #end.size = (400,400)
    #end.position = (400,200)
    #board.game_over = True
    #board.stop()

@bird.register
def on_key_pressed_space(self):
    self.physics.velocity_y = 200
    if board.is_running is False and not board.game_over:
        board.start()
        
@bird.register
def act(self):
    print(bird.physics._body.position)

board.run()

