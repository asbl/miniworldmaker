Kollisionen und Sensoren
=================

Zusätzlich zu den Reaktionen auf Ereignisse können Tokens auch über Sensoren den Status des Boards überprüfen und ob z.B. andere Tokens sich an gleicher Stelle befinden.

Dies geht z.B. mit folgender Funktion:

### Ein Objekt aufspüren

Du kannst ein Token folgendermaßen aufspüren:

```
@player.register
def on_sensing_token(self, token):
    print("Damage!!!!!")
    self.remove()
```

### Vergleichen mit Objekt

Oft soll eine Aktion nur ausgeführt werden, wenn ein *bestimmtes* Objekt aufgespürt wird. Dies geht z.B. so:

```
@player1.register
def on_sensing_token(self, token):
    if token == player2:
      print(token == player2)
```

### Grenzen des Spielfelds überprüfen


Du kannst auch überprüfen, ob eine Spielfigur an den Grenzen des Spielfelds ist (oder darüber hinaus):

Nicht auf dem Spielfeld:

```
@player3.register
def on_sensing_not_on_board(self):
  print("Warning: I'm not on the board!!!")
```

An den Grenzen des Spielfelds:

```
@player4.register
def on_sensing_borders(self, borders):
  print("Borders are here!", str(borders))
```

Befindet sich eine Spielfigur an der Position (0,0) wird folgendes ausgegeben:

`Borders are here! ['right', 'top'`



Die Objekte können auf unterschiedliche Art aufgespürt werden. Dies kann über die Eigenschaft `collision_type` des aufspürenden Objekts eingestellt werden, z.B. "mask" für einen pixelgenauen Vergleich oder 'rect' wenn nur die umschließenden Rechtecke verglichen werden.

> ➥ Mehr über Sensoren: [Key Concept: Sensors](../key_concepts/sensors.md)