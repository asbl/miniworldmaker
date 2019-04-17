from miniworldmaker import *
import easygui


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=30, rows=20, tile_size=20, tile_margin=0)
        for i in range(self.rows):
            for j in range(self.columns):
                self.add_to_board(Grass(), (j, i))
        wall = self.add_to_board(Wall(), (0, 4))
        self.add_to_board(Wall(), (1, 4))
        self.add_to_board(Wall(), (2, 4))
        self.add_to_board(Wall(), (3, 4))
        self.add_to_board(Wall(), (4, 4))
        self.add_to_board(Wall(), (5, 4))
        self.add_to_board(Wall(), (6, 4))
        self.add_to_board(Wall(), (6, 0))
        self.add_to_board(Wall(), (6, 1))
        self.add_to_board(Wall(), (6, 3))
        self.torch = self.add_to_board(Torch(), (10, 4))
        self.fireplace = self.add_to_board(Fireplace(), (10, 14))
        self.door = self.add_to_board(Door(), (6, 2))
        self.add_to_board(Player(), (8, 2))
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.toolbar = Toolbar()
        self._window.add_container(self.toolbar, "right")
        self.console = self._window.add_container(Console(), "bottom")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/knight.png")
        self.costume.is_rotatable = False
        self.inventory = []

    def move(self, distance=1):
        walls = self.sensing_tokens(token=Wall)
        doors = self.sensing_tokens(token=Door)
        closed_doors = [door for door in doors if door.closed is True]
        if not walls and not closed_doors and self.sensing_on_board():
            super().move()

    def get_event(self, event, data):
        print(event, data)
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
            fireplace = self.sensing_token(distance=0, token=Fireplace)
            print(fireplace)
            if fireplace:
                print("burn")
                self.board.console.newline("Du zündest die Feuerstelle an.")
                self.board.fireplace.burn()

    def act(self):
        torch = self.sensing_token(distance=0, token=Torch)
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
        actors_in_front = self.sensing_tokens(distance = 1, token = Door)
        if self.board.door in actors_in_front:
            if self.board.door.closed:
                message = "Die Tür ist geschlossen... möchtest du sie öffnen"
                choices = ["Ja", "Nein"]
                reply = easygui.buttonbox(message, "RPG", choices)
                if reply == "Ja":
                    self.board.door.open()
                    self.board.console.newline("Du hast das Tor geöffnet.")


class Wall(Token):

    def __init__(self):
        super().__init__()
        self.is_blocking = True
        self.add_image("rpgimages/wall.png")


class Grass(Token):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/grass.png")


class Torch(Token):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/torch.png")


class Fireplace(Token):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/fireplace_0.png")
        burned = self.add_costume("rpgimages/fireplace_1.png")
        burned.add_image("rpgimages/fireplace_2.png")
        self.burning = False
        self.is_static = True

    def burn(self):
        if self.burning == False:
            self.board.play_sound("rpgsounds/fireplace.wav")
            self.switch_costume()
            self.costume.is_animated = True


class Door(Token):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/door_closed.png")
        self.add_costume("rpgimages/door_open.png")
        self.closed = True
        self.is_static = True

    def open(self):
        if self.closed == True:
            self.switch_costume()
            self.board.play_sound("rpgsounds/olddoor.wav")
            self.closed = False


my_grid = MyBoard()
my_grid.show()
