# Position, Ausrichtung und Bewegung

In diesem Kapitel lernst du, wie du Position und Ausrichtung eines Tokens verändern kannst, um es zu bewegen.

## move() und position

Es gibt zwei Möglichkeiten ein Token zu bewegen:

* Mit dem `position`-Attribut kannst du direkt die Position eines Tokens verändern.
* Die Funktion `move` bewegt dein Token in die aktuelle Richtung.
Die aktuelle Richtung kannst du mit `token.direction` festlegen, z.B. so:

## position

Die Position kannst du z.B. so verändern:

``` python
@player.register
def act(self):
    self.position = (100, 200) # places token at x = 100, y = 200
```

### Beispiel

In diesem Beispiel wird das Token immer wieder (Alle 50 Frames) an eine zufällige Position bewegt:

``` python
import miniworldmaker as mwm
import random

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token((100, 100))
player.add_costume("images/target.png")
player.orientation = -90

@player.register
def act(self):
    if self.board.frame % 50 == 0: # every 50th frame:
        player.position = (random.randint(0, 400), random.randint(0, 400))

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/target1.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## x und y

Alternativ kannst du auch direkt mit den Attributen `x` und `y` einzelne Koordinaten des Tokens verändern:

``` python
@player.register
def act(self):
    self.x = 100 # places token at x = 100.
```

**Beispiel:**

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((90,90))
player.add_costume("images/player.png")
player.costume.orientation = -90 
@player.register
def on_key_down_w(self):
    player.y = player.y - 1

player2 = mwm.Token((180,180))
player2.add_costume("images/player.png")
player2.costume.orientation = -90 
@player2.register
def on_key_pressed_s(self):
    player2.y = player2.y - 1
    
board.run()
```

 <video controls loop width=100%>
  <source src="../_static/keydown.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Die move()-Funktion

Die Funktion `move()` kannst du in Kombination mit dem Attribut `direction` oder der Funktion `turn_left` bzw. `turn_right` aufrufen:

``` python
@player.register
def act(self):
    self.direction = "right" # can also be 90
    self.move()
    # Alternative with turn_left:
    self.turn_left(30) # turns 30° left
    self.move()
```

**Beispiel:**

Das Token schaut nach rechts und bewegt sich dann einen Schritt vor:

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.direction = "right"
    self.move()

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/moveright.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## move_left, move_right, ...

Mit der Funktion move() bewegt sich das `Token` immer in die aktuelle `direction`. 

Du kannst das `Token` aber auch direkt in eine Richtung bewegen lassen. Dies geht mit den Befehlen `move_right()`, `move_left()`, `move_up()` und `m̀ove_down()`.

Das Programm oben würde so aussehen:

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.move_right()

board.run()
```

## move_in_direction

Alternativ kannst du das Token mit `move_in_direction()` auch in eine beliebige Richtung bewegen.

Beispiel: Das Token bewegt sich schräg nach oben

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((100,100))
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.move_in_direction(45)

board.run()

```

 <video controls loop width=100%>
  <source src="../_static/movedirection.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

### Beispiel: Bewegung in Mausposition

Das folgende Programm steuert mit Hilfe der Funktion `move_in_direction()` das Token in Richtung des Mauszeigers:

``` python
import miniworldmaker as mwm

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90

@player.register
def act(self):
    self.move_in_direction(self.board.get_mouse_position())

board.run()

```

 <video controls loop width=100%>
  <source src="../_static/followmouse.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## turn_left und turn_right

Mit `turn_left()` und `turn_right` kannst du das Token in eine Richtung drehen.

* ``player.turn_left(degrees)`` - Dreht das Token um **degrees** Grad nach links.
* ``player.turn_right(degrees)`` - Dreht das Token um **degrees** Grad nach rechts.

Beispiel:

``` python
import miniworldmaker as mwm

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token((100, 100))
player.add_costume("images/player.png")
player.orientation = -90

@player.register
def act(self):
    self.move()
    
@player.register
def on_key_down_a(self):
    self.turn_left(30)

@player.register
def on_key_down_d(self):
    self.turn_right(30)


board.run()
```

 <video controls loop width=100%>
  <source src="../_static/turn.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Direction

Mit `self.direction` kannst du die aktuelle Richtung des Tokens abfragen oder ändern
  
Der Wert degrees kann hier entweder als Zahl oder als Text wie in folgender Grafik angegeben werden (0: oben, 180, unten, 90 rechts, -90 links):

![Move on board](/_images/movement.jpg)
  
Beispiel:

Im folgenden Beispiel bewegt sich das Token im Kreis:

``` python
import miniworldmaker as mwm

board = mwm.Board(400,400)
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90
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
