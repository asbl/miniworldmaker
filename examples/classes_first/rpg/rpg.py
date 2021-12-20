import easygui
from miniworldmaker import *

class MyBoard(TiledBoard):

    def on_setup(self):
        self.columns = 30
        self.rows = 20
        self.tile_size = 20
        self.add_background((255,255,255,0))
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
        self.toolbar = self.add_container(Toolbar(), "right")
        self.console = self.add_container(Console(), "bottom")
        print("setup finished")

    def on_message(self, data):
        if data == "Fackel":
            fireplace = self.player.sensing_token(Fireplace)
            if fireplace:
                self.console.newline("Du zündest die Feuerstelle an.")
                self.fireplace.burn()


class Player(Token):

    def on_setup(self):
        self.add_costume("rpgimages/knight.png")
        self.costume.is_rotatable = False
        self.inventory = []

    def on_key_down_w(self):
        self.move_up()

    def on_key_down_s(self):
        self.move_down()

    def on_key_down_a(self):
        self.move_left()

    def on_key_down_d(self):
        self.move_right()

    def on_sensing_torch(self, torch):
        message = "Du findest eine Fackel. Möchtest du sie aufheben?"
        choices = ["Ja", "Nein"]
        reply = easygui.buttonbox(message, "RPG", choices)
        if reply == "Ja":
            self.inventory.append("Torch")
            self.board.torch.remove()
            self.board.console.newline("Du hebst die Fackel auf.")
        self.board.toolbar.add_widget(ToolbarButton("Fackel", "rpgimages/torch.png"))

    def on_sensing_wall(self, wall):
        self.move_back()

    def on_sensing_door(self, door):
        if door.closed:
            self.move_back()
            message = "Die Tür ist geschlossen... möchtest du sie öffnen"
            choices = ["Ja", "Nein"]
            reply = easygui.buttonbox(message, "RPG", choices)
            if reply == "Ja":
                self.board.door.open()
                self.board.console.newline("Du hast das Tor geöffnet.")


class Wall(Token):

    def on_setup(self):
        self.add_costume("rpgimages/wall.png")
        self.static = True


class Grass(Token):

    def on_setup(self):
        self.add_costume("rpgimages/grass.png")
        self.static = True

class Torch(Token):

    def on_setup(self):
        self.add_costume("rpgimages/torch.png")


class Fireplace(Token):

    def on_setup(self):
        self.add_costume("rpgimages/fireplace_0.png")
        self.costume_burned = self.add_costume(["rpgimages/fireplace_1.png", "rpgimages/fireplace_2.png"])
        self.burning = False

    def burn(self):
        if self.burning == False:
            self.board.play_sound("rpgsounds/fireplace.wav")
            self.switch_costume(self.costume_burned)
            self.costume.is_animated = True


class Door(Token):

    def on_setup(self):
        self.add_costume("rpgimages/door_closed.png")
        self.costume_open = self.add_costume("rpgimages/door_open.png")
        self.closed = True

    def open(self):
        if self.closed == True:
            self.switch_costume(self.costume_open)
            self.board.play_sound("rpgsounds/olddoor.wav")
            self.closed = False


my_grid = MyBoard()
my_grid.run(fit_desktop = True)