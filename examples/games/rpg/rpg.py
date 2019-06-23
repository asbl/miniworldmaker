import easygui
from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=30, rows=20, tile_size=20, tile_margin=0)
        for i in range(self.rows):
            for j in range(self.columns):
                Grass((j, i))
        Wall((0, 4))
        Wall((1, 4))
        Wall((2, 4))
        Wall((3, 4))
        Wall((4, 4))
        Wall((5, 4))
        Wall((6, 4))
        Wall((6, 0))
        Wall((6, 1))
        Wall((6, 3))
        self.torch = Torch((10, 4))
        self.fireplace = Fireplace((10, 14))
        self.door = Door((6, 2))
        self.player = Player((8, 2))
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.toolbar = self._window.add_container(Toolbar(), "right")
        self.console = self._window.add_container(Console(), "bottom")

    def get_event(self, event, data):
        if event == "button" and data == "Fackel":
            fireplace = self.player.sensing_token(distance=0, token_type=Fireplace)
            if fireplace:
                self.console.newline("Du zündest die Feuerstelle an.")
                self.fireplace.burn()


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


    def on_key_down(self, keys):
        if "W" in keys:
            self.point_in_direction("up")
            self.move()
        elif "S" in keys:
            self.point_in_direction("down")
            self.move()
        elif "A" in keys:
            self.point_in_direction("left")
            self.move()
        elif "D" in keys:
            self.point_in_direction("right")
            self.move()

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
            self.is_blocking = False
            self.closed = False


my_grid = MyBoard()
my_grid.show()
