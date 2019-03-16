from gamegridp import *


class MyGrid(CellGrid, GUIGrid,  AudioGrid):

    def __init__(self):
        super().__init__(cell_size=20, columns=30, rows=20, margin=1)
        for i in range(self.rows):
            for j in range(self.columns):
                self.add_actor(Grass(), (j, i))
        wall = self.add_actor(Wall(),(0,4))
        self.add_actor(Wall(), (1, 4))
        self.add_actor(Wall(), (2, 4))
        self.add_actor(Wall(), (3, 4))
        self.add_actor(Wall(), (4, 4))
        self.add_actor(Wall(), (5, 4))
        self.add_actor(Wall(), (6, 4))
        self.add_actor(Wall(), (6, 0))
        self.add_actor(Wall(), (6, 1))
        self.add_actor(Wall(), (6, 3))
        self.torch = self.add_actor(Torch(), (10, 4))
        self.fireplace = self.add_actor(Fireplace(), (10, 14))
        self.door = self.add_actor(Door(), (6,2))
        self.add_actor(Player(), (8, 2))
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.toolbar = Toolbar()
        self._window.add_container(self.toolbar, "right")
        self.console = Console()
        self._window.add_container(self.console, "bottom")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/knight.png")
        self.image_action("rotate", False)
        self.inventory = []

    def act(self):
        pass

    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.move(direction = "up")
            elif "S" in data:
                self.move(direction = "down")
            elif "A" in data:
                self.move(direction = "left")
            elif "D" in data:
                self.move(direction = "right")
        actors_at_position = self.grid.get_actors_at_location(self.look())
        print(actors_at_position)
        if event == "button" and data == "Fackel":
            if self.grid.fireplace in actors_at_position:
                self.grid.console.print("Du zündest die Feuerstelle an.")
                self.grid.fireplace.burn()
        if self.grid.torch in actors_at_position:
            message = "Du findest eine Fackel. Möchtest du sie aufheben?"
            choices = ["Ja", "Nein"]
            reply = self.grid.button_box(message, choices)
            if reply == "Ja":
                self.inventory.append("Torch")
                self.grid.torch.remove()
                self.grid.console.print("Du hebst die Fackel auf.")
                self.grid.toolbar.add_widget(ToolbarButton("Fackel", "rpgimages/torch.png"))
        # look forward
        actors_in_front = self.grid.get_actors_at_location(self.look(direction = "forward"))
        if self.grid.door in actors_in_front:
            if self.grid.door.closed:
                message = "Die Tür ist geschlossen... möchtest du sie öffnen"
                choices = ["Ja", "Nein"]
                reply = self.grid.button_box(message, choices)
                if reply == "Ja":
                    self.grid.door.open()
                    self.grid.console.print("Du hast das Tor geöffnet.")


class Wall(Actor):

    def __init__(self):
        super().__init__()
        self.is_blocking = True
        self.add_image("rpgimages/wall.png")


class Grass(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/grass.png")


class Torch(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/torch.png")


class Fireplace(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/fireplace_0.png")
        self.burning = False
        self.is_static = True

    def burn(self):
        if self.burning == False:
            self.clear()
            self.add_image("rpgimages/fireplace_1.png")
            self.add_image("rpgimages/fireplace_2.png")
            self.grid.play_sound("rpgsounds/fireplace.wav")
            self.animate()
            self.burning = True


class Door(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("rpgimages/door_closed.png")
        self.is_blocking = True
        self.closed = True
        self.is_static = True

    def open(self):
        if self.closed == True:
            self.clear()
            self.add_image("rpgimages/door_open.png")
            self.grid.play_sound("rpgsounds/olddoor.wav")
            self.closed = False
            self.is_blocking = False


my_grid = MyGrid()
my_grid.show_log()
my_grid.show()
