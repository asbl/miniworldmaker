import sqlite3 as lite
from miniworldmaker import *
import easygui


class MyBoard(TiledBoard):

    def __init__(self, **kwargs):
        super().__init__(rows=12, columns=12, tile_size=40)
        self.register_token_type(Robot)
        self.register_token_type(Wall)
        self.register_token_type(Gold)
        self.register_token_type(Diamond)
        self.register_token_type(Emerald)
        self.create_world_toolbar = SelectTokenTypeToolbar(self)
        self.create_world_toolbar.add_widget(SaveButton("db_files/ctw_db.db", self, "Save"))
        self.create_world_toolbar.add_widget(LoadButton("db_files/ctw_db.db", self, "Load", ))
        self._window.add_container(self.create_world_toolbar, "right")
        self.event_console = EventConsole()
        self.event_console.register_events = {"all"}
        self._window.add_container(self.event_console, "right", size=500)
        self.add_image(path="images/stone.jpg")

    def get_event(self, event, data):
        if event == "mouse_left":
            position = self.get_board_position_from_pixel(data)
            actor = self.add_to_board(self.create_world_toolbar.selected_actor(), position=position)
        elif event == "mouse_right":
            position = self.get_board_position_from_pixel(data)
            self.remove_tokens_in_area(position)


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")


class Wall(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/rock.png")


class Gold(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/stone_gold.png")


class Diamond(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/stone_blue.png",)


class Emerald(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/stone_green.png")


my_board = MyBoard()
my_board.show()
