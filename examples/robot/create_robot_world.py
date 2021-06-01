from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.create_world_toolbar = LevelDesignerToolbar(self)
        self.create_world_toolbar.add_widget(SaveButton(filename="db_files/ctw_db.db", board=self, text="Save"))
        self.create_world_toolbar.add_widget(LoadButton(filename="db_files/ctw_db.db", board=self, text="Load", ))
        self._window.add_container(self.create_world_toolbar, "right")
        self.event_console = EventConsole()
        self._window.add_container(self.event_console, "right", size=500)
        self.add_image(path="images/stone.jpg")


class Robot(Actor):

    def on_setup(self):
        self.add_image("images/robo_green.png")


class Wall(Token):

    def on_setup(self):
        self.add_image("images/rock.png")


class Gold(Token):

    def on_setup(self):
        self.add_image("images/stone_gold.png")


class Diamond(Token):

    def on_setup(self):
        self.add_image("images/stone_blue.png",)
        print("Diamond created at", self.position)


class Emerald(Token):

    def on_setup(self):
        self.add_image("images/stone_green.png")


my_board = MyBoard(12, 12)
my_board.show()
