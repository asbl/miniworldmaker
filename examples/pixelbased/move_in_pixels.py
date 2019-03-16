from gamegridp import *


class MyGrid(PixelGrid):
    """My Grid with custom setup method."""

    def __init__(self):
        super().__init__(cell_size=1, columns=200, rows=200, margin=0)
        player1 = Player()
        self.add_actor(player1, position=(30, 30))
        self.add_image("images/soccer_green.jpg")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")

    def act(self):
        self.move()

    def get_event(self, event, data):
        if event == "key":
            if "W" in data:
                self.move("up")
            elif "S" in data:
                self.move("down")
            elif "A" in data:
                self.move("left")
            elif "D" in data:
                self.move("right")


mygrid = MyGrid()
mygrid.title="My Grid"
mygrid.show()
