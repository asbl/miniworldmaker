import random
import miniworldmaker as mwm

board = mwm.PixelBoard(800, 600)
board.game_over = False
board.add_background("images/background.png")
pipes = []
pipes.append(mwm.Token(position=(260, board.height - 280)))
pipes.append(mwm.Token(position=(520, 0)))
pipes.append(mwm.Token(position=(780, board.height - 280)))
pipes.append(mwm.Token(position=(760, -100)))
for pipe in pipes:
    pipe.add_costume("images/pipe1.png")
    pipe.costume.is_rotatable = False
    pipe.size = (80, 300)
    pipe.passed = False
    pipe.speed = 5
    pipe.physics.gravity = False
    pipe.start_physics()

    @pipe.register
    def act(self):
        self.move_in_direction("left")
        if self.position.x < 75 and self.passed is False:
            self.passed = True
            score.inc()
            
    @pipe.register
    def on_sensing_left_border(self):
        self.move_to(position=mwm.BoardPosition(self.position.x + random.randint(750, 800), self.y))
        self.passed = False
        
pipes[1].costume.orientation = -180
pipes[3].costume.orientation = -180

score = mwm.NumberToken()
score.position = (30, 30)
score.size = (40, 40)
board.stop()
bird = mwm.Token()
bird.position = (75, 200)
bird.add_costume("images/fly.png")
bird.size = (60, 60)
bird.costume.orientation = 180
bird.flip_x()
bird.physics.size = (0.8, 0.8)
bird.physics.shape_type = "circle"

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
    end=mwm.TextToken()
    end.set_text("Game over!")
    end.position = (400,200)
    board.game_over = True
    board.stop()

@bird.register
def on_key_pressed_space(self):
    self.physics.velocity_y = 200
    if board.is_running is False and not board.game_over:
        board.start()
bird.start_physics()
board.run()

