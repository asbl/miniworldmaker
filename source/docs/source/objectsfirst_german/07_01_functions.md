# Funktionen

Du hast bisher Methoden verwendet, die zu einem Board oder einem Token gehören, z.B. ``on_setup``, ``act``.

## Definieren von Funktionen

Oft willst du komplizierte Dinge automatisieren, z.B. das Anlegen von Tokens. 

Dies geht, indem du Funktionen selbst definierst - Dies geht z.B. so:

```python
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

```python
create_token(4,2)
```

Hier wird ein Token an der Position x=4 und y=2 angelegt.

## Umfangreiches Beispiel

Das folgende Beispiel ist eine Vorlage, die deinen Code kürzer gestaltet, wenn du Funktionen verwendest. 

Es werden hier 10 Tokens mit 10 Befehlen angelegt. Ohne Funktionen hättest du 30 Befehle benötigt.

```python
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