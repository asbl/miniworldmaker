# Sensoren

Tokens verfügen über **Sensoren**, mit denen sie ihre Umwelt abtasten 
können und z.B andere Tokens an ihrer Position aufspüren können.

## Ein Objekt aufspüren

Ein `Token` kann ein anderes `Token` am selben Ort aufspüren, indem du die 
Funktion `on_sensing_token` registrierst.

```python
@player.register
def on_sensing_token(self, other):
    print("Damage!!!!!")
    self.remove()
```

### Was passiert hier?

* Die Funktion `on_sensing_token` wird dann aufgerufen, wenn das Token
    ein anderes Objekt am selben Ort aufspürt.
* Der Parameter `other` ist ein Verweis auf das gefundene Objekt, so
    dass du direkt auf Attribute und Methoden dieses Objektes zugreifen
    kannst (z.B. mit `other.move()`)

## Vergleichen mit gefundenem Objekt

Oft soll eine Aktion nur ausgeführt werden, wenn ein *bestimmtes* Objekt
aufgespürt wird.

Dies geht z.B. so:

```{code-block} python
---
lineno-start: 1
---
@player1.register
def on_sensing_token(self, other):
    global player2
    if other == player2:
      print("I found you, player2!")
```

Der Vergleich in Zeile 6 überprüft, ob das Objekt **dasselbe** Objekt
ist wie `player2`.

```{note}
**Exkurs: Globale Variablen**: Normalerweise sind Variablen nur
innerhalb einer Methode bekannt, damit z.B. verhindert wird, dass es zu
Seiteneffekten kommt, wenn man an verschiedenen Stellen auf die gleiche
Variable zugreift.
```

Der Ansatz mit dem hier auf Variablen aus anderen Programmteilen
zugegriffen wird ist zwar einfach und intuitiv - Später wird man aber
versuchen dies zu vermeiden.

### Umfangreiches Beispiel

Der folgende Code zeigt, wie du verhindern kannst, dass sich Objekte durch Wände hindurch bewegen können:

```python
from miniworldmaker import *

board = TiledBoard()
board.columns = 8
board.rows = 2
board.speed = 30
player = Token()
player.add_costume("images/player_1.png")

wall = Token((4,0))
wall.add_costume("images/wall.png")

@player.register
def act(self):
    if player.position != (0,4):
        player.direction = "right"
        player.move()

@player.register
def on_sensing_token(self, other):
    if other==wall:
        self.move_back()
    

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/wall.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 

## Weitere Sensoren

### Grenzen des Spielfelds überprüfen

Du kannst auch überprüfen, ob eine Spielfigur an den Grenzen des
Spielfelds ist (oder darüber hinaus):

*Ist die Figur nicht auf dem Spielfeld?*

```python
@player3.register
def on_sensing_not_on_board(self):
  print("Warning: I'm not on the board!!!")
```

*Ist die Figur an den Grenzen des Spielfelds?*

```python
@player4.register
def on_sensing_borders(self, borders):
  print("Borders are here!", str(borders))
```

Befindet sich eine Spielfigur an der Position (0,0) wird folgendes
ausgegeben: [Borders are here! \[\'right\', \'top\'\]]{.title-ref}

## FAQ

-   Meine Kollisionen werden nicht erkannt, was kann ich tun?

    Teste zunächst, ob die Methode überhaupt aufgerufen wird, z.B. mit:

    ``` python
    @player.register
    def on_sensing_token(self, token):
      print(token)
      ...
    ```

    Wenn die `print`-Anweisung nicht aufgerufen wird, dann funktioniert
    der Sensor nicht.

## Ausblick

* Mehr Informationen. Siehe
    `Key Concepts: Sensors <../key_concepts/sensors>`{.interpreted-text
    role="doc"}.
* Die Objekte können auf unterschiedliche Art aufgespürt werden. Dies
    kann über die Eigenschaft `collision_type` des aufspürenden Objekts
    eingestellt werden, z.B. \"mask\" für einen pixelgenauen Vergleich
    oder \'rect\' wenn nur die umschließenden Rechtecke verglichen
    werden.
