Physik
========

Erstelle zunächst einige einfache Objekte:

```
from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((0, 0, 0, 255))
        self.line1 = Line((0, 100), (600, 800), 5)
        self.line2 = Line((50, 400), (300, 400),5)
        self.circle1 = Circle((70, 20), 5, 0)
        self.line3 = Line((0, 350), (600, 400), 10)
        self.box = Rectangle((300, 90), 80, 80, 0)
        self.box.image.fill((90, 255, 0, 220))

my_board = MyBoard(800, 600)
my_board.show()

```

Du kannst nun in folgenden Schritten die Physikeigenschaften festlegen:

 1. Lege Eigenschaften fest:
 
    * friction (>0): Die Reibung des Objektes
    * elasticity (zwischen 0 und 1): Die Elastizität des Objektes
    * Gravity (True or False): Reagiert das Objekt auf Gravität?
    * mass (>0): Die Masse des Objekts
    * can_move: Kann das Objekt bewegt werden?
    * stable: Hat das Objekt ein Drehmoment?
    * shape_type ("line", "rect", oder "circle") - Wie soll die Physikengine das Objekt behandelt=
 
 2. Starte die Physikengine:
 
```
   # Lege zuerst die Eigenschaften fest
   self.circle1.mass = 5
   # Starte dann die Physikengine
   self.circle1.start_physics()
```

  3. Lege einen Impuls an Objekte an:
```
   # Lege zuerst die Eigenschaften fest
   self.circle1.mass = 5
   # Starte dann die Physikengine
   self.circle1.start_physics()
   # Lege einen Impuls an:
   self.circle1.velocity_x = 500
   self.circle1.velocity_y = 100
```
  