import easygui
from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=30, rows=20, tile_size=20, tile_margin=0)
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.toolbar = Toolbar()
        self._window.add_container(self.toolbar, "right")
        self.console = self._window.add_container(Console(), "bottom")
        self.door = None


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("rpgimages/knight.png")
        self.costume.is_rotatable = False
        self.inventory = []
        self.is_blocking = False

    def move(self, distance=1):
        tokens = self.sensing_tokens()
        doors = self.sensing_tokens(token_type=Door)
        closed_doors = [door for door in doors if door.closed is True]
        blocking = [token for token in tokens if token.is_blocking is True]
        if not blocking and not closed_doors and self.sensing_on_board():
            super().move()

    def get_event(self, event, data):
        if event == "key_down":
            direction = None
            if "W" in data:
                self.point_in_direction("up")
                self.move()
            elif "S" in data:
                self.point_in_direction("down")
                self.move()
            elif "A" in data:
                self.point_in_direction("left")
                self.move()
            elif "D" in data:
                self.point_in_direction("right")
                self.move()
        if event == "button" and data == "Fackel":
            fireplace = self.sensing_token(distance=0, token_type=Fireplace)
            if fireplace:

                self.board.console.newline("Du zündest die Feuerstelle an.")
                self.board.fireplace.burn()

    def act(self):
        torch = self.sensing_token(distance=0, token_type=Torch)
        if torch:
            message = "Du findest eine Fackel. Möchtest du sie aufheben?"
            choices = ["Ja", "Nein"]
            reply = easygui.buttonbox(message, "RPG", choices)
            if reply == "Ja":
                self.inventory.append("Torch")
                self.board.torch.remove()
                self.board.console.newline("Du hebst die Fackel auf.")
            self.board.toolbar.add_widget(ToolbarButton("Fackel", "rpgimages/torch.png"))
        # look forward
        actors_in_front = self.sensing_tokens(distance = 1, token_type = Door)
        if self.board.door:
            if self.board.door in actors_in_front:
                if self.board.door.closed:
                    message = "Die Tür ist geschlossen... möchtest du sie öffnen"
                    choices = ["Ja", "Nein"]
                    reply = easygui.buttonbox(message, "RPG", choices)
                    if reply == "Ja":
                        self.board.door.open()
                        self.board.console.newline("Du hast das Tor geöffnet.")


class Wall(Token):

    def __init__(self, position):
        super().__init__(position)
        self.is_blocking = True
        self.add_image("rpgimages/wall.png")


class Grass(Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("rpgimages/grass.png")
        self.is_blocking = False


class Torch(Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("rpgimages/torch.png")
        self.is_blocking = False


class Fireplace(Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("rpgimages/fireplace_0.png")
        burned = self.add_costume("rpgimages/fireplace_1.png")
        burned.add_image("rpgimages/fireplace_2.png")
        self.burning = False
        self.is_blocking = False

    def burn(self):
        if self.burning == False:
            self.board.play_sound("rpgsounds/fireplace.wav")
            self.switch_costume()
            self.costume.is_animated = True


class Door(Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("rpgimages/door_closed.png")
        self.add_costume("rpgimages/door_open.png")
        self.closed = True
        self.is_blocking = True

    def open(self):
        if self.closed == True:
            self.switch_costume()
            self.board.play_sound("rpgsounds/olddoor.wav")
            self.closed = False
            self.is_blocking = False

board = MyBoard.from_db("data.db")
board.window.send_event_to_containers("Loaded new world", "data.db")
board.show()
