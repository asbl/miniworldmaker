from gamegridp import *


class MyGrid(CellGrid):
    def __init__(self):
        super().__init__(cell_size=40, columns=29, rows=1, margin=0)
        robot1 = Robot()
        robot1.add_image("images/robo_green.png")
        self.add_actor(robot1, position=(0, 0))
        robot2 = Robot()
        robot2.add_image("images/robo_yellow.png")
        robot2.turn_left(180)
        self.add_actor(robot2, position=(28, 0))
        self.add_image(img_path="images/water.png")

    def act(self):
        pass

    def get_event(self, event, data):
        if event == "collision":
            for robot in data:
                robot.remove()
            explosion = Explosion()
            self.add_actor(explosion, position=data[0].position)



class Explosion(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/explosion.png")


class Robot(Actor):
    def __init__(self):
        super().__init__()

    def act(self):
        self.move()

my_grid = MyGrid()
my_grid.speed = 50
my_grid.show()
