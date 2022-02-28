# Dynamik

Du kannst bis jetzt ein Board erstellen und Tokens darauf gestalten.
Diese können sich aber noch nicht bewegen.

## Die act()-Methode

Das Spielfeld und alle Tokens können über die Methode `act()` gesteuert
werden. Diese Methode wird immer wieder aufgerufen (genau genommen: Alle
`board.speed` Zeiteinheiten) bis das Spiel beendet wird.

![First Token](../_images/act.png)

Wenn du ein Token erstellst, kannst du mit dem Decorator `@register`
eine `act()`-Methode zum Spielfeld oder zu deinen Token hinzufügen:

### Beispiel

```{code-block} python
---
lineno-start: 1
---
from miniworldmaker import *

board = TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
player = Token()
player.add_costume("images/player_1.png")
player.direction = 90
@player.register
def act(self):
    self.move()

board.run()
```

#### Was passiert hier?

Zeile 12-14: Der Decorator `@player.register` bindet die Methode `act`
an das Objekt `player`.

Auf ähnliche Weise wirst du später öfters Reaktionen auf Events bei
Objekten registrieren (z.B. Reaktionen auf Tastatur- oder Mauseingaben
oder Kollisionsüberprüfungen).

 <video controls loop width=100%>
  <source src="../_static/moving_token.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Das Schlüsselwort self

In dem code oben hast du gesehen, dass die Methode ``act`` als Parameter das Schlüsselwort ``self`` erwartet. 

Alle Methoden die zu einem Objekt gehören erhalten dieses Schlüsselwort immer als ersten Paramerer.

Anschließend kann innerhalb der Methode mit diesem Schlüsselwort auf Attribute und Methoden des Objekts selbst zurückgegriffen werden.

Beispiel:

Dieser Code

```python
@player.register
def act(self):
    self.direction = "right"
```

ist äquivalent zu diesem Code:

```python
@player.register
def act(self):
    player.direction = "right"
```

``self`` bezieht sich hier auf das ``player``-Objekt, bei dem die Methode registriert wurde.

## Die Frame Rate - Wie oft wird act() aufgerufen?


Man kann einstellen, wie oft ``act()`` aufgerufen wird, indem man die Attribute ``board.fps`` und ``board.speed`` konfiguriert.

* ``board.fps`` definiert die ``frame rate``. Analog zu einem Daumenkino, bei dem du mit festgelegter Geschwindigkeit die Seiten umblätterst, 
  definiert die Framerate wie oft pro Sekunde das Bild neu gezeichnet wird.
  ``board.fps`` hat den Standardwert 60, d.h. es werden 60 Bilder pro Sekunde angezeigt.
  
* Im Attribut ``board.frame`` wird der aktuelle frame gespeichert. Die Frames seit Programmstart werden hochgezählt.
  
* ``board.speed`` definiert wie oft die Programmlogik (z.B. act) pro Sekunde aufgerufen wird. 
  Ein Wert von 60 bedeutet, dass die act()-Methode jeden 60. Frame aufgerufen wird.


```python
  from miniworldmaker import *

  board = PixelBoard()
  board.size = (120,210)

  @board.register
  def on_setup(self):
      board.fps = 1
      board.speed = 3
      
  @board.register
  def act(self):
      print(board.frame)

  board.run()
```

Das Programm oben hat die Ausgabe:

```
  3
  6
  9
  12
  15
```


Es wird sehr langsam hochgezählt, weil genau ein Frame pro Sekunde abgespielt wird und jeden 3. Frame
(also alle 3 Sekunden) die Funktion ``act()`` aufgerufen wird.



## Ausblick

-   [Vollständiges
    Beispiel](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/03%20-%20actions.py)
-   [Weitere
    Beispiele](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tests/2%20Movement)
