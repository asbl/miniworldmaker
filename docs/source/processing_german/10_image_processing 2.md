# Bildbearbeitung II (mit Funktionen)

## Helligkeit

Oft benötigen wir die Helligkeit eines Pixels. Die "einfachste Methode dies zu berechnen ist den Durchschnitt der r,g und b-Werte zu berechnen:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

print(brightness(arr[10][20]))
 
board.background.from_array(arr)
board.run()
```

In der Funktion brightness müssen die Werte r, g und b zunächst umgewandelt werden:
Es handelt sich um `uint8`-Werte, so dass das Ergebnis niemals größer als 255 werden darf (Ansonsten ensteht ein "Overflow"). Deshalb müssen die Variablen in den Datentyp `int` umgewandelt werden, damit das Ergebnis der Addition auch ein `int`-Wert und damit beliebig groß ist.

Dies können wir nutzen, um jeden Pixel grau zu färben, abhängig von seiner Helligkeit:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

for x in range(len(arr)):
    for y in range(len(arr[0])):
        
        arr[x][y] = brightness(arr[x][y][0], arr[x][y][1], arr[x][y][2])
        
board.background.from_array(arr)
board.run()
```

![grey](../_images/sunflower5_grey.png)