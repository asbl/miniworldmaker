# Ereignisse und Bewegung

Typische Aktionen in einem Brettspiel sind das Setzen und das Bewegen von Tokens.

Es gibt verschiedene Arten von Bewegung:

## Setzen des Tokens an einer Position


## Verschieben des Tokens mit Drag and Drop

Um ein Token zu verschieben, müssen die Events `on_mouse_left` sowie `on_mouse_left_released` registriert werden.
Außerdem muss man den aktuellen Zustand in irgendeiner Form speichern, d.h. ob das Token gerade verschoben wird,
z.B. durch ein Attribut `dragged`, welches man zu dem Token hinzufügt.

``` python
from miniworldmaker import *
board = TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 40
board.add_background("images/stone.png")
board.background.is_textured = True
t1 = Token((0,0))
t2 = Token((3,4))
t1.add_costume("images/player_blue.png")
t2.add_costume("images/player_red.png")

@t2.register
def on_mouse_left(self, mouse_pos):
    if self.sensing_point(mouse_pos):
        self.dragged = True
        
@t2.register
def on_mouse_left_released(self, mouse_pos):
    tile = board.get_tile(mouse_pos)
    if not board.is_mouse_pressed():
        self.dragged = False
        self.position = tile
        
board.run()
```
