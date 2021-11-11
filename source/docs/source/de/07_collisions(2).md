Kollisionen und Sensoren II
=================

Ein typischer Anwendungsfall ist es herauszufinden, welche Art von **Token** berührt wurde. 

Es gibt für dieses Problem mehrere Lösungen:

## Attribut token_type

Du kannst all deinen Objekten ein Objekt ein Attribut token_type hinzufügen:

```
player2 = miniworldmaker.Token()
wall = miniworldmaker.Token()
player2.token_type = "actor"
wall.token_type = "wall"

@player1.register
def on_sensing_token(self, other_token):
    if other_token.token_type == "actor":
        pass # tue etwa
    elif other_token.token_type == "wall":
        pass # tue etwas anders
```

:::{important} 
Bei diesem Zugang musst du **jedem** Objekt ein Attribut `token_type` geben. Ansonsten musst du auch überprüfen, ob dieses überhaupt vorhanden ist, wenn du nicht möchtest, dass ansonsten dein komplettes Programm abstürzt.

Dies kann man machen mit:
```
if  other_token.token_type and other_token.token_type == "actor":
```
Wenn jedes token über das Attribut `token_type` verfügt, dann kannst du diese Abfrage auch weglassen.
:::  

## Listen

Du kannst Objekte zu einer Liste hinzufügen um zu überprüfen, ob das berührte Objekt in dieser Liste ist.

```
walls = []
player2 = miniworldmaker.Token()
wall = miniworldmaker.Token()
walls.append(wall)

@player1.register
def on_sensing_token(self, other_token):
    if other_token.token_type in walls:
        pass # tue etwas
```

:::{important} 
Bei diesem Zugang musst du darauf achten, dass gelöschte Objekte auch aus der Liste entfernt werden z.B. auf folgende Art und weise:
``` 
walls.remove(wall)
wall.remove()
```
:::  

## Klassen

Wenn du mit Klassen arbeitest, nimmt dir der **miniworldmaker** etwas Arbeit ab, weil er nun selbst erkennen kann, um welche **Kindklasse** von `Token` es sich bei einem Objekt handelt.

Hier kannst du zu deiner Klasse folgende Methode hinzufügen:

`def on_sensing_[klassenname](self, other)`

### Beispiel:

```python
# Die Andere Klasse hat den Namen Torch
def on_sensing_torch(self, torch):
    print("Sensing torch")
    # ...
```

### Vollständiges Beispiel

```
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.Token((2,6))
player1.add_costume("images/player_1.png")
player2 = miniworldmaker.Token((5,3))
player2.add_costume("images/player_1.png")
player2.token_type = "actor"
walls = []
for i in range(5):
    wall = miniworldmaker.Token((i,i))
    wall.token_type = "wall"
    wall.add_costume("images/wall.png")
    walls.append(wall)

@player1.register
def on_sensing_token(self, other_token):
    if other_token.token_type == "actor":
        pass # tue etwa
    elif other_token.token_type == "wall":
        pass # tue etwas anders

@player1.register
def on_key_down_w(self):
    self.move_up()
@player1.register
def on_key_down_a(self):
    self.move_left()
@player1.register
def on_key_down_d(self):
    self.move_right()
@player1.register
def on_key_down_s(self):
    self.move_down()
    
@player1.register
def on_sensing_token(self, other):
    if other in walls:
        self.move_back()
board.run()
```



