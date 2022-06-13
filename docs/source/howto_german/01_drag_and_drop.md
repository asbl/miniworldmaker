# Drag and Drop

Um ein Token zu verschieben, müssen die Events `on_mouse_left` sowie `on_mouse_left_released` registriert werden.
Dann benötigt man eine Variable (z.B. `dragged`), in der man den Zustand speichert, d.h. ob ein Objekt gerade verschoben wird. 

 <video controls loop width=100%>
  <source src="../_static/draganddrop.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

* Wenn die Maus geklicked wird, dann wird der Zustannd der Variable `dragged`auf `True` gesetzt.
* Wenn die Maus losgelassen wird, dann wird das Token nur dann verschoben, wenn `dragged` auf `True` gesetzt ist. Danach wird `dragged` wieder auf `False` gesetzt.

## Beispiele:

Kreise verschieben:

``` python
from miniworldmaker import *

board = Board(200, 200)
circle = Circle((30, 30), 60)
circle.direction = 90
circle.dragged = False

@circle.register
def on_mouse_left(self, mouse_pos):
    if self.sensing_point(mouse_pos):
        self.dragged = True
        
@circle.register
def on_mouse_left_released(self, mouse_pos):
    if self.dragged:
        self.dragged = False
        self.center = mouse_pos
        
board.run()
```

Drag and Drop auf einem TiledBoard:

``` python
from miniworldmaker import *
board = TiledBoard()
t1 = Token((0,0))
t2 = Token((3,4))
t2.dragged = False

@t2.register
def on_mouse_left(self, mouse_pos):
    print(self.sensing_point(mouse_pos))
    if self.sensing_point(mouse_pos):
        self.dragged = True
        print("start drag")
        
@t2.register
def on_mouse_left_released(self, mouse_pos):
    tile = board.get_board_position_from_pixel(mouse_pos)
    print("released")
    if self.dragged:
        self.position = tile
        print("end drag")
    self.dragged = False
        
board.run()
```



