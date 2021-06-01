import sqlite3 as lite

from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=60,
                         columns=10,
                         rows=10,
                         tile_margin=0)
        self.add_image(path="images/stone.jpg")
        self.file = "robot01.db"
        self.load()

    def load(self):
        connection = lite.connect(self.file)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Actors')
        for actordata in cursor.fetchall():
            if actordata[3] == "Wall":
                self.add_to_board(Wall(), position=(actordata[1], actordata[2]))
            elif actordata[3] == "Robot":
                self.add_to_board(Robot(), position=(actordata[1], actordata[2]))
        actors = cursor.fetchall()
        print("Load Actors: " + str(actors))


class Robot(Token):

    def __init__(self):
        super().__init__()
        self.title = "Robot"
        self.is_rotatable = True
        self.add_image("images/robo_green.png")


class Wall(Token):

    def __init__(self):
        super().__init__()
        self.title = "Wall"
        self.is_blocking = True
        self.add_image("images/rock.png")


class Gold(Token):

    def __init__(self):
        super().__init__()
        self.title = "Wall"
        self.add_image("images/stone_gold.png")


class Diamond(Token):
    def __init__(self):
        super().__init__()
        self.title = "Wall"
        self.add_image("images/stone_blue.png", )


class Emerald(Token):
    def __init__(self):
        super().__init__()
        self.title = "Wall"
        self.add_image("images/stone_green.png")


mygrid = MyBoard()
mygrid.show()
