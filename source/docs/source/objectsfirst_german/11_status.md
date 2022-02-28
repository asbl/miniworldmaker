# Status: Spielstand/Spielende/Levels

## Status/Punktestand

- Oft willst du den aktuellen Punktestand oder ähnliches anzeigen.

Hierfür bietet dir der **miniworldmaker** spezielle Tokens an, z.B.
Text oder Number-Tokens.

### Einen Text erstellen

Einen Text kannst du so erstellen:

```python
text = miniworldmaker.Text(position, string)
```

- position ist ein Tupel mit der oberen Linken Ecke des Textes
- string ist ein Text, der angzeigt wird.

Auf einem Pixelboard wird ein Text automatisch skaliert.
Auf einem Tiledboard wird dieser komplett innerhalb einer Kachel angezeigt 
(und ist damit bei längeren Texten vermutlich zu klein)

#### Beispiel:

```python
from miniworldmaker import *

board = PixelBoard(400,400)
hallo_welt = Text((100,100), "Hallo Welt!")

board.run()
```

<img src="../_images/text1.png" width=260px alt="Texts"/>

### Einen Text verändern

Mit dem Attribut text kannst du den Text jederzeit verändern.

Das folgende Programm zeigt immer den zuletzt gedrückten Button an:

```python
from miniworldmaker import *

board = PixelBoard(400,400)
key = Text((100,100), "")

@key.register
def on_key_down(self, key):
    print(key)
    self.text = key[0]

board.run()
```

<img src="../_images/text2.png" width=260px alt="Texts and Events"/>

## Zahlen

Zahlen kannst du mit Number-Tokens auf den Bildschirm anzeigen.

Dies funktionier sehr ähnlich wie bei Texten. Das folgende Programm erhöht z.B. 
jedesmal wenn eine Taste gedrückt wird die angezeigt Zahl um 1:

```python
from miniworldmaker import *

board = PixelBoard(400,400)
show_number = Number((100,100), 1)

@show_number.register
def on_key_down(self, key):
    n = self.get_number()
    self.set_number(n + 1)

board.run()
```



## Spielende / Levelwechsel

Zum Spielende/Levelwechsel sind folgendes typische Aktionen:

-   Das Spielfeld löschen
-   Das Spielfeld anhalten.

Dafür gibt es folgende Befehle:

-   `board.stop()`: Stoppt das Spielfeld. Es werden keine Aktionen mehr
    ausgeführt und keine Events abgefragt.
-   `board.start()`: Dies hebt einen Stop-Befehl auf.
-   `board.is_running`: Mit dieser Variable kannst du den Status des
    Spielfelds abfragen.
-   `board.clear()`: Die Funktion entfernt alle Figuren vom Spielfeld.
-   `board.reset()`: Die Funktion löscht das aktuelle Spielfeld und
    erstellt ein neues Spielfeld mit allen Figuren so wie sie in
    [board.on_setup()]{.title-ref} erzeugt wurden.


