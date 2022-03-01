# Funktionen

Du hast bisher Methoden verwendet, die zu einem Board oder einem Token gehören, z.B. ``on_setup``, ``act``.

## Definieren von Funktionen

Oft willst du komplizierte Dinge automatisieren, z.B. das Anlegen von Tokens. 

Dies geht, indem du Funktionen selbst definierst - Dies geht z.B. so:

``` python
def create_token(x, y):
    t = Token()
    t.position = (x,y)
    t.add_costume("images/player.png")
```

Deine Funktion besteht aus einer *Signatur* und einem *Funktionskörper*.

* Die Signatur ist die erste Zeile der Funktion. Sie enthält alle Informationen
  die du brauchst um die Funktion aufzurufen. Dies ist der **Name** und **Parameter**.
  Der Name dieser Funktion ist `create_token`, die Parameter sind `x`und `y`. 
  Paramter werden benötigt um der Funktion weitere Informationen zu übergeben, in diesem Fall
  die Informationen **wo** das Token erstellt werden soll.

* Der Funktionskörper ist ein Code-Block. Er enthält alle Befehle, die bei Aufruf der Funktion 
  nacheinander abgearbeitet werden.
  
  Hier wird beim Funktionsaufruf zuerst ein Token angelegt und anschließend 
  werden die Eigenschaften des Tokens definiert.

## Aufruf von Funktionen

Eine Funktion wird mit Hilfe des Namens aufgerufen. Dabei übergibst du der Funktion die als Parameter definierten Argumente. 
Dies kann z.B. so aussehen:

``` python
create_token(4,2)
```

Hier wird ein Token an der Position x=4 und y=2 angelegt.

## Tokens automatisiert erstellen

Mit Hilfe von Funktionen kannst du das erstellen von Tokens abkürzen:

Es werden hier 10 Tokens mit 10 Befehlen angelegt. Ohne Funktionen hättest du 30 Befehle benötigt.

``` python
from miniworldmaker import *

board = TiledBoard()
board.rows = 8

def create_token(x, y):
    t = Token()
    t.position = (x,y)
    t.add_costume("images/player.png")

def create_wall(x, y):
    t = Token()
    t.position = (x,y)
    t.add_costume("images/wall.png")
    
create_token(4,2)
create_wall(4,4)
create_wall(5,4)
create_wall(6,4)
create_wall(6,3)
create_wall(6,2)
create_wall(6,1)
create_wall(5,1)
create_wall(4,1)
create_wall(3,1)

board.run()
```

Ausgabe: 

![walls](../_images/walls.png)

## Eigenschaften und Methoden registrieren.

Das folgende Programm erstellt automatisch "Regentropfen".

In der funktion raindrop werden nicht nur Eigenschaften für jeden Tropfen festgelegt, sondern auch Methoden registriert.

```python
from miniworldmaker import *
import random

board = Board()
board.add_background((80,180,255))
def raindrop(x,y):
    c = Circle((x, y), random.randint(10, 20))
    speed = random.randint(1,5)
    c.color = (0,0,random.randint(100,255), 100)
    c.static = True
    @c.register
    def act(self):
        self.move_down(random.randint(1,3))
    @c.register
    def on_sensing_not_on_board(self):
        self.remove()
        
@board.register
def act(self):
    if board.frame % 5 == 0:
        raindrop(random.randint(0,400),0)
    

board.run()
```

 <video controls loop width=450px>
  <source src="../_static/raindrops.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 