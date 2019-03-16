import sqlite3 as lite
from gamegridp import *


class MyGrid(CellGrid, DatabaseGrid, GUIGrid):

    def __init__(self):
        super().__init__(cell_size=60, columns=10, rows=10,
                margin=0)
        self.toolbar = Toolbar()
        self._window.add_container(self.toolbar, "right")
        self.toolbar.add_widget(ToolbarButton("Speichern", "images/save.png", ))
        self.toolbar.add_widget(ToolbarButton("Laden", "images/save.png", ))
        self.toolbar.add_widget(ToolbarButton("Wall", "images/rock.png", ))
        self.toolbar.add_widget(ToolbarButton("Robot", "images/robo_green.png", ))
        self.toolbar.add_widget(ToolbarButton("Gold", "images/stone_gold.png", ))
        self.toolbar.add_widget(ToolbarButton("Diamond", "images/stone_blue.png", ))
        self.toolbar.add_widget(ToolbarButton("Emerald", "images/stone_green.png",))
        self.state= "wall"
        self.add_image( img_path="images/stone.jpg")

    def get_event(self, event, data):
        if event == "mouse_left":
            position = self.pixel_to_cell(data)
            if self.is_empty_cell((data[0], data[1])):
                if self.state=="wall":
                    actor = self.add_actor(Wall(), position = (position))
                elif self.state=="robot":
                    actor =  self.add_actor(Robot(), position = (position))
                elif self.state=="gold":
                    actor =  self.add_actor(Gold(), position = (position))
                elif self.state=="diamond":
                    actor =  self.add_actor(Diamond(), position = (position))
                elif self.state=="emerald":
                    actor =  self.add_actor(Emerald(), position = (position))
            else:
                self.remove_actors_from_location(position)
            print(position)
        elif event == "button":
            if data == "Robot":
                self.state="robot"
            elif data == "Wall":
                self.state="wall"
            elif data == "Gold":
                self.state="gold"
            elif data == "Emerald":
                self.state="emerald"
            elif data == "Diamond":
                self.state="diamond"
            elif data=="Speichern":
                game_id = self.save()
                self.message_box("Neues Spiel mit id "+str(game_id)+" erstellt")
            if data=="Laden":
                game_id=self.integer_box("Gebe das Spiel ein, das geladen werden soll")
                if game_id:
                    self.remove_all_actors()
                    self.load(game_id)

    def save(self) -> int:
        self.connect("robodatabase.db")
        row = self.select_single_row('SELECT id FROM Game ORDER BY id DESC LIMIT 1')
        gameid = row[0]
        gameid=gameid+1
        for actor in self.actors:
            dict = {"column":actor.position[0],
                                  "row": actor.position[1],
                                  "GameID": gameid,
                                  "Actor" : actor.title}
            self.insert("Actors", dict )
        self.insert("Game",{"ID": gameid})
        self.commit()
        self.close_connection()
        return gameid

    def load(self, game_id):
        connection = lite.connect('robodatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Actors WHERE GameID=' + str(game_id))
        for actordata in cursor.fetchall():
            if actordata[4]=="Wall":
                self.add_actor(Wall(), position=(actordata[1],actordata[2]))
            elif actordata[4]=="Robot":
                self.add_actor(Robot(), position=(actordata[1], actordata[2]))
        actors=cursor.fetchall()
        print("Load Actors: "+str(actors))


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.title="Robot"
        self.is_rotatable = True
        self.add_image("images/robo_green.png")

class Wall(Actor):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.is_blocking = True
        self.add_image("images/rock.png")


class Gold(Actor):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_gold.png")


class Diamond(Actor):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_blue.png",)


class Emerald(Actor):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_green.png")


mygrid = MyGrid()
mygrid.show()
