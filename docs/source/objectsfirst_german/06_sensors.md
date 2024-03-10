# Sensoren

Tokens verfügen über **Sensoren**, mit denen sie ihre Umwelt abtasten 
können und z.B andere Tokens an ihrer Position aufspüren können.

## Ein Objekt aufspüren.

Du kannst Objekte aufspüren, indem du die entsprechenden Sensoren direkt aufrufst.
Dies geht z.B. so:

``` python
import miniworldmaker as mwm

board = mwm.Board(200, 100)

r = mwm.Rectangle((10,10),50,100)
c = mwm.Circle((200,50),20)

@c.register
def act(self):
    self.move_left()

@r.register
def act(self):
    token = self.detect()
    if token:
        self.color = (255,0,0)

board.run()
```

Die zweite `act()`-Methode enthält den Sensor. Mit der Methode `self.detect` wird abgefragt, welche Tokens
an der aktuellen Stelle gefunden wurde. Falls kein Token gefunden wird, gibt die Methode `None` zurück.

:::{note}
Die Anweisung `if token` ist äquivalent zu
`if token != None`.
:::

Wenn das Rechteck mit seinen Sensoren ein anderes `Token` aufspürt, dann ändert sich die Farbe.

 <video controls loop width=300px>
  <source src="../_static/sensor.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Ereignisse

In dem Beispiel oben wurde *aktiv* nach Tokens gesucht. Alternativ dazu kannst du auch ein Ereignis registrieren,
dass automatisch dann aufgerufen wird, wenn der Sensor des Tokens etwas aufspürt:

Das letzte Programm kann mit Hilfe von Ereignissen so programmiert werden:

``` python
from miniworldmaker import *

board = mwm.Board(200, 100)

r = mwm.Rectangle((10,10),50,100)
c = mwm.Circle((200,50),20)

@c.register
def act(self):
    self.move_left()
 
@r.register
def on_detecting(self, other):
    self.color = (255,0,0)

board.run()
```

Was passiert hier?

* Die registrierte Funktion `on_detecting` wird dann aufgerufen, wenn das Token
  ein anderes Objekt am selben Ort aufspürt.
* Der Parameter `other` ist ein Verweis auf das gefundene Objekt. Du kannst diesen benutzen
  um herauszufinden, welches andere Token gefunden wurde. 

## Was wurde gefunden?

Mit Hilfe von Sensoren und if-else Verzweigungen kannst du herausfinden, was genau gefunden wurde.
Dies geht z.B. so:

``` python
import miniworldmaker as mwm

board = Board(200, 100)

r = Rectangle((10,10),50,100)

c1 = mwm.ircle((200,50),20)
c2 = mwm.Circle((120,50),20)

@c1.register
def act(self):
    self.move_left()

@c2.register
def act(self):
    self.move_left()
    
@r.register
def on_detecting(self, other):
    if other == c1:
        self.color = (255,0,0)
    if other == c2:
        self.color = (0, 255,0)

board.run()
```

In der on_detect_token-Methode wird überprüft, ob `other` das gleiche Objekt ist wie `c1` bzw. `c2`.

Wenn dies zutrifft, wird das Rechteck entsprechend eingefärbt.

 <video controls loop width=300px>
  <source src="../_static/sensor2.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

``` {note}
**Exkurs: Globale Variablen**: Normalerweise sind Variablen nur
innerhalb einer Methode bekannt, damit z.B. verhindert wird, dass es zu
Seiteneffekten kommt, wenn man an verschiedenen Stellen auf die gleiche
Variable zugreift.


Der Ansatz mit dem hier auf Variablen aus anderen Programmteilen
zugegriffen wird ist zwar einfach und intuitiv - Im Tutorial `classes_first`
wirst du lernen, wie man dies vermeiden kann.
```

### Wände

Der folgende Code zeigt, wie du verhindern kannst, dass sich Objekte durch Wände hindurch bewegen können.
Auch dies lässt sich mit Hilfe von Sensoren ermöglichen:

``` python
import miniworldmaker as mwm

board = mwm.TiledBoard()
board.columns = 8
board.rows = 2
board.speed = 30
player = mwm.Token()
player.add_costume("images/player_1.png")

wall = mwm.Token((4,0))
wall.add_costume("images/wall.png")

@player.register
def act(self):
    if player.position != (0,4):
        player.direction = "right"
        player.move()

@player.register
def on_detecting(self, other):
    if other==wall:
        self.move_back()
    

board.run()
```

 <video controls loop width=300px>
  <source src="../_static/wall.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Weitere Sensoren

### Grenzen des Spielfelds überprüfen

Du kannst auch überprüfen, ob eine Spielfigur an den Grenzen des
Spielfelds ist (oder darüber hinaus):

*Ist die Figur nicht auf dem Spielfeld?*

``` python
@player3.register
def on_not_detecting_board(self):
  print("Warning: I'm not on the board!!!")
```

Beispiel:

Das folgende Programm simuliert einen umherschwimmenden Fisch:

``` python
import miniworldmaker as mwm

board = TiledBoard()
board.columns = 4
board.rows = 1
board.add_background("images/water.png")
fish = mwm.Token((0,0))
fish.add_costume("images/fish.png")
fish.costume.orientation = - 90
fish.direction = "right"
@fish.register
def act(self):
    self.move()

@fish.register
def on_not_detecting_board(self):
    self.move_back()
    self.flip_x()
        
board.run()
```

 <video controls loop width=300px>
  <source src="../_static/flipthefish.webm" type="video/webm">
  Your browser does not support the video tag.
</video>


*Ist die Figur an den Grenzen des Spielfelds?*

``` python
@player4.register
def on_detecting_borders(self, borders):
  print("Borders are here!", str(borders))
```

Befindet sich eine Spielfigur an der Position (0,0) wird folgendes
ausgegeben: `Borders are here! ['right', 'top']`

## FAQ

* Meine Kollisionen werden nicht erkannt, was kann ich tun?

  Teste zunächst, ob die Methode überhaupt aufgerufen wird, z.B. mit:

  ``` python
  @player.register
  def on_detecting(self, token):
    print(token)
    ...
  ```

  Wenn die `print`-Anweisung nicht aufgerufen wird, dann funktioniert
  der Sensor nicht.