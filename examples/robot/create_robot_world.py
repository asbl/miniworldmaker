import sqlite3 as lite
from miniworldmaker import *
import easygui


class MyBoard(TiledBoard):

    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = Toolbar()
        self._window.add_container(self.toolbar, "right")
        self.toolbar.add_widget(ToolbarButton("Speichern", "images/save.png", ))
        # self.toolbar.add_widget(ToolbarButton("Laden", "images/save.png", ))
        self.toolbar.add_widget(ToolbarButton("Wall", "images/rock.png", ))
        self.toolbar.add_widget(ToolbarButton("Robot", "images/robo_green.png", ))
        self.toolbar.add_widget(ToolbarButton("Gold", "images/stone_gold.png", ))
        self.toolbar.add_widget(ToolbarButton("Diamond", "images/stone_blue.png", ))
        self.toolbar.add_widget(ToolbarButton("Emerald", "images/stone_green.png",))
        self.state= "wall"
        self.add_image(path="images/stone.jpg")
        self.file = file
        self.init_database()

    def init_database(self):
        query1 = """     CREATE TABLE IF NOT EXISTS `Actors` (
                        `id`			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `column`		INTEGER,
                        `row`			INTEGER,
                        `actor_class`	TEXT
                        );
                        """
        query2 = """     CREATE TABLE IF NOT EXISTS `board` (
                        `tile_size`		ITEGER
                        `rows`			INTEGER
                        `columns`		INTEGER,
                        `row`			INTEGER,
                        `margin`	    INTEGER
                        );
                        """
        with lite.connect(self.file) as db:
            cur = db.cursor()
            cur.execute(query1)
            cur.execute(query2)
            db.commit()

    def get_event(self, event, data):
        if event == "mouse_left":
            position = self.to_board_position(data)
            if self.is_empty_cell((data[0], data[1])):
                if self.state=="wall":
                    actor = self.add_to_board(Wall(), position=(position))
                elif self.state=="robot":
                    actor = self.add_to_board(Robot(), position=(position))
                elif self.state=="gold":
                    actor = self.add_to_board(Gold(), position=(position))
                elif self.state=="diamond":
                    actor = self.add_to_board(Diamond(), position=(position))
                elif self.state=="emerald":
                    actor = self.add_to_board(Emerald(), position=(position))
        elif event == "mouse_right":
            position = self.to_board_position(data)
            self.remove_tokens_in_area(position)
            print("mouse-right", position)
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
                easygui.msgbox("Spiel wurde in Datei {0} gespeichert".format(self.file))
            if data=="Laden":
                game_id = easygui.fileopenbox("Gebe das Spiel ein, das geladen werden soll")
                if game_id:
                    self.remove_all_actors()
                    self.load()

    def save(self):
        self.connect(self.file)
        for actor in self.tokens:
            dict = {"column": actor.position[0],
                    "row": actor.position[1],
                    "actor_class": actor.class_name}
            self.insert("Actors", dict )
        self.commit()
        self.close_connection()

    def load(self):
        connection = lite.connect(self.file)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Actors')
        for actordata in cursor.fetchall():
            if actordata[3] == "Wall":
                self.add_to_board(Wall(), position=(actordata[1], actordata[2]))
            elif actordata[3] == "Robot":
                self.add_to_board(Robot(), position=(actordata[1], actordata[2]))
        actors=cursor.fetchall()
        print("Load Actors: "+str(actors))


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.title="Robot"
        self.is_rotatable = True
        self.add_image("images/robo_green.png")


class Wall(Token):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.is_blocking = True
        self.add_image("images/rock.png")


class Gold(Token):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_gold.png")


class Diamond(Token):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_blue.png",)


class Emerald(Token):
    def __init__(self):
        super().__init__()
        self.title="Wall"
        self.add_image("images/stone_green.png")


modus = easygui.buttonbox("Neue Welt erstellen oder alte Welt laden",
                          "Neue Welt / Laden", ["Neue Welt", "Laden"])
print(modus)
if modus == "Neue Welt":
    file = easygui.filesavebox("Gebe an, in welcher Datei das Spiel gespeichert werden soll.",
                               "Speicherort auswählen", "database.db", ".db")
    rows = easygui.integerbox("Gebe die Anzahl an *Zeilen* ein", "Zeilen")
    columns = easygui.integerbox("Gebe die Anzahl an *Spalen* ein", "Spalten")
    tile_size = easygui.integerbox("Gebe die Größe der Kacheln an", "Tile-Size", 64)
    margin = easygui.integerbox("Gebe den Abstand zwischen den Kacheln an", "Margin", 1)
    mygrid = MyBoard(rows=rows, columns=columns, tile_size=tile_size, file=file, tile_margin=margin)
else:
    file = easygui.fileopenbox("Gebe die Datei an", "Datei auswählen", "database.db", ".db", False)
    mygrid = MyBoard(file=file)
    mygrid.load()

mygrid.show()
