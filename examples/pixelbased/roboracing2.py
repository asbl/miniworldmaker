from gamegridp import *


class MyGrid(GameGrid):

    def __init__(self):
        super().__init__(cell_size=1, columns=200, rows=200, margin=0)
        self.add_image(img_path = "images/stone.jpg")
        self.add_actor(Robot(), position = (50,50))


class Robot(Actor):

    def __init__(self):
        super().__init__()
        self.size= (30,30)
        self.add_image("images/robo_green.png")

    def act(self):
        pass

    def get_event(self, event, data):
        if event == "key":
            if "A" in data:
                self.turn_left(10)
            if "D" in data:
                self.turn_right(10)
            if "W" in data:
                self.move(distance = 3)


mygrid = MyGrid()
mygrid.show()
