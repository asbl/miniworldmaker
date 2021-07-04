import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)
board.add_background("images/stone.jpg")
board.fps = 60
robot = miniworldmaker.Token(position=(50, 50))
robot.add_costume("images/robo_green.png")
robot.costume.orientation = - 90
robot.size = (30,30)
@robot.register
def act(self):
    global board
    print(board.speed)
    mouse_pos = board.get_mouse_position()
    if mouse_pos:
        self.point_towards_position(mouse_pos)
        self.move()
               
board.run()
