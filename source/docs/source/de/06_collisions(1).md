Kollisionen und Sensoren
=================

Zusätzlich zu den Reaktionen auf Ereignisse können Tokens auch über **Sensoren** überprüfen, ob sich z.B. andere Tokens an der gleichen Stelle befinden.

### Ein Objekt aufspüren

Ein `Token` kann ein anderes `Token` am selben Ort folgendermaßen aufspüren:

```python
@player.register
def on_sensing_token(self, other):
    print("Damage!!!!!")
    self.remove()
```

  * Die Funktion `on_sensing_token` wird dann aufgerufen, wenn das Token ein anderes Objekt am selben Ort aufspürt. 
  
  * Der Parameter `other` ist ein Verweis auf das gefundene Objekt, so dass du direkt auf Attribute und Methoden dieses Objektes zugreifen kannst (z.B. mit `other.move()`)

### Vergleichen mit Objekt

Oft soll eine Aktion nur ausgeführt werden, wenn ein *bestimmtes* Objekt aufgespürt wird. Dies geht z.B. so:

```{code-block} python
---
lineno-start: 1
emphasize-lines: 1,5,6
---
player 2 = miniworldmaker.Token()
...
@player1.register
def on_sensing_token(self, other):
    global player2
    if other == player2`:
      print("I found you, player2!")
```

Der Vergleich in Zeile 6 überprüft, ob das Objekt **dasselbe** Objekt ist wie `player2`. 

#### Exkurs: Globale Variablen

Normalerweise sind Variablen nur innerhalb einer Methode bekannt, damit z.B. verhindert wird, dass es zu Seiteneffekten kommt, wenn man an verschiedenen Stellen auf die gleiche Variable zugreift. Der Ansatz mit dem hier auf Variablen aus anderen Programmteilen zugegriffen wird ist zwar einfach und intuitiv - Später wird man aber versuchen dies zu vermeiden.

### Grenzen des Spielfelds überprüfen


Du kannst auch überprüfen, ob eine Spielfigur an den Grenzen des Spielfelds ist (oder darüber hinaus):

#### Ist die Figur nicht auf dem Spielfeld?

```python
@player3.register
def on_sensing_not_on_board(self):
  print("Warning: I'm not on the board!!!")
```

#### Ist die Figur an den Grenzen des Spielfelds?

```python
@player4.register
def on_sensing_borders(self, borders):
  print("Borders are here!", str(borders))
```

Befindet sich eine Spielfigur an der Position (0,0) wird folgendes ausgegeben:

`Borders are here! ['right', 'top']`

### Vollständiges Beispiel

```{code-block} python
---
lineno-start: 1
emphasize-lines: 1,5,6
---
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.Token()
player1.add_costume("images/player_1.png")
player2 = miniworldmaker.Token((8, 0))
player2.add_costume("images/player_1.png")
@player1.register
def act(self):
    self.direction = 90
    if not self.sensing_tokens():
        self.move()
@player1.register
def on_sensing_token(self, other):
    global player2
    if other == player2:
      print("I found you!")
board.run()
```

### FAQ

  - Meine Kollisionen werden nicht erkannt, was kann ich tun?

    * Teste zunächst, ob die Methode überhaupt aufgerufen wird, z.B. mit:

    ```python
    @player.register
    def on_sensing_token(self, token):
      print(token)
      ...
    ```

    Wenn die `print`-Anweisung nicht aufgerufen wird, dann funktioniert der Sensor nicht.


### Ausblick

Die Objekte können auf unterschiedliche Art aufgespürt werden. Dies kann über die Eigenschaft `collision_type` des aufspürenden Objekts eingestellt werden, z.B. "mask" für einen pixelgenauen Vergleich oder 'rect' wenn nur die umschließenden Rechtecke verglichen werden.




> ➥ Mehr über Sensoren: [Key Concept: Sensors](../key_concepts/sensors.md)