# Bewegung und Ausrichtung 

Mit der ``act(self)``-Methode kannst du Token in regelmäßigen Abständen ansteuern. Jetzt lernst du, wie du deine Token gezielt in eine Richtung bewegen kannst.

## Die move()-Funktion


Die zentrale Funktion zum Bewegen ist die Funktion `move()`.

Mit der Funktion `move()` kannst du dein Objekt um einen oder mehrere Schritte bewegen:

### Beispiel

``` python
@player.register
def act(self):
    self.direction = "right"
    self.move()
```

Das Token `player` schaut nach rechts und bewegt sich dann einen Schritt nach vorne.
Dies wird regelmäßig wiederholt, wenn die Methode act() aufgerufen wird.

Vollständiges Beispiel:

``` python
from miniworldmaker import *

board = TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
player = Token()
player.add_costume("images/player_1.png")
@player.register
def act(self):
    self.direction = "right"
    self.move()

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/moving_token.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## move_left, move_right, ...

Mit der Funktion move() bewegt sich das `Token` immer in die aktuelle `direction`. 

Du kannst das `Token` aber auch direkt in eine Richtung bewegen lassen. Dies geht mit den Befehlen `move_right()`, `move_left()`, `move_up()` und `m̀ove_down()`.

### Beispiel

Dieser Code bewegt das Token in der act()-Methode nach rechts:

``` python
@player.register
def act(self):
    self.move_right()
```

## move_in_direction

Alternativ kannst du das Token mit `move_in_direction()` auch in eine beliebige Richtung bewegen.

### Beispiel:


Dies bewegt das Token schräg rechts nach oben (Richtung 45°). 

``` python
@player.register
def act(self):
    self.move_in_direction(45)
```

### Umfangreiches Beispiel

Bewegung in Richtung der Mausposition:

``` python
import miniworldmaker

board = miniworldmaker.PixelBoard()
board.columns = 400
board.rows = 400
board.add_background("images/soccer_green.jpg")
player = miniworldmaker.Token()
player.add_costume("images/player_1.png")

@player.register
def act(self):
    self.move_in_direction(self.board.get_mouse_position())

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/followmouse.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 


## Die Richtung ändern

Die Richtung kannst du mit folgenden Befehlen ändern:

* ``player.turn_left(degrees)`` - Dreht das Token um **degrees** Grad nach links.
* ``player.turn_right(degrees)`` - Dreht das Token um **degrees** Grad nach rechts.
* ``player.direction = degrees``- Gibt dem player-Objekt die absolute Ausrichtung degrees.
  
Der Wert degrees kann hier entweder als Zahl oder als Text wie in folgender Grafik angegeben werden (0: oben, 180, unten, 90 rechts, -90 links):

![Move on board](/_images/movement.jpg)
  
### Beispiel:

`self.direction = 90` bezieht sich z.B. *auf die eigene* Ausrichtung, `self.move_in_direction()` ruft die eigene Methode `move_in_direction` auf.

### Umfangreiches Beispiel

Im folgenden Beispiel bewegt sich das Token im Kreis:

``` python
from miniworldmaker import *

board = PixelBoard()
board.columns = 400
board.rows = 400
board.add_background("images/soccer_green.jpg")
player = Token()
player.add_costume("images/player_1.png")
player.position = (200, 200)

@player.register
def act(self):
    self.direction = self.board.frame
    self.move()
    

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/move_in_circle.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Ausblick

* Mehr Informationen. Siehe [Key Concepts: Movement](../key_concepts/movement)
* Mehr Informationen. Siehe [Key Concepts: Directions](../key_concepts/directions)