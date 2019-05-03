from miniworldmaker import *

class MyBoard(PixelBoard):

    def __init__(self):
        height, width = 500, 280
        super().__init__(columns=width, rows=height)
        self.background.add_image("images/background.png")
        self.add_to_board(Bird(), (75, 200))
        self.pipe1 = self.add_to_board(Pipe(top=False), (260, height - 260) )
        self.pipe2 = self.add_to_board(Pipe(top=True), (520, 0) )
        self.score = self.add_to_board(NumberToken(0),(0, 0))
        self.score.size = (80,80)


class Bird(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/flappy.png")
        self.size = (100, 100)
        self.v_y = 1

    def act(self):
        gravity = 0.3
        self.v_y += gravity
        self.move_to(position = BoardPosition(self.position.x, self.y+self.v_y))
        borders = self.sensing_borders()
        if "bottom" in borders or "top" in borders:
            self.board.is_running = False
        pipes = self.sensing_token(token = Pipe, exact= True)
        if pipes:
            self.board.is_running = False

    def get_event(self, event, data):
        if event == "key_pressed" and "SPACE" in data:
            self.v_y = -5


class Pipe(Actor):

    def __init__(self, top):
        super().__init__()
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