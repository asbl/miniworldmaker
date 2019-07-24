Bewegungen
==========

### Die Move-Funktion

Die zentrale Funktion zum Bewegen ist die Funktion move

Move hat folgende Signatur:

```
    def move(distance) -> BoardPosition:
```

Dies bedeutet:
  
  * Standardmäßig bewegt sich ein Akteur um **self.speed** Schritte in die Richtung in die er gerade schaut.
  
  * Du kannst die Distanz die er sich bewegt aber auch manuell festlegen, indem du für den Paramter distance einen Integer-Wert einsetzt.
  
  * Die Funktion gibt als Rückgabewert die Position auf dem Spielfeld zurück, an der sich der Akteur nach dem Zug befindet.
  
### Methoden und Attribute

Bewegt ein Akteur.

```eval_rst
.. autoclass:: miniworldmaker.tokens.token.Token
   :members: move
   :noindex:
```