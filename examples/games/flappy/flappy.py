from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        height, width = 500, 280
        super().__init__(columns=width, rows=height)
        self.background.add_image("images/background.png")
        Bird((75, 200))
        self.pipe1 = Pipe(top=False, position= (260, height - 260))
        self.pipe2 = Pipe(top=True, position= (520, 0))
        self.score = NumberToken(position = (0, 0), number=0)
        self.score.size = (80, 80)
        self.is_running = False


class Bird(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/fly.png")
        self.size = (60, 60)
        self.start_physics()
        self.costume.orientation = 180
        self.flip_x()

    def act(self):
        borders = self.sensing_borders()
        if "bottom" in borders or "top" in borders:
            self.board.is_running = False
        pipes = self.sensing_token(token_type=Pipe, exact=True)
        if pipes:
            self.board.is_running = False
            self.board.reset()

    def on_key_pressed(self, keys):
        if "SPACE" in keys:
            self.physics.velocity_y = 200
            if self.board.is_running is False:
                self.board.is_running = True


class Pipe(Actor):

    def __init__(self, top, position):
        super().__init__(position)
        self.add_image("images/pipe1.png")
        self.size = (80, 260)
        self.passed = False
        self.speed = 5
        if top:
            self.costume.orientation = -180

    def act(self):
        self.move_in_direction("left")
        if "left" in self.sensing_borders():
            self.move_to(position = BoardPosition(self.position.x+520, self.y) )
            self.passed = False
        if self.position.x < 75 and self.passed is False:
            self.passed = True
            self.board.score.inc()


board = MyBoard()
board.show()