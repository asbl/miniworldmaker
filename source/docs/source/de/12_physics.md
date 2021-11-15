Physik
======

Die Physikengine kannst du mit Hilfe eines `Physicboard`s verwenden: In einem Physikboard funktionieren einige Bewegungs- und Kollissionsfunktionen etwas anders als auf anderen Boards:

## Erste Schritte

Erstelle zunächst ein Physicsboard und darin ein Token:

```
import miniworldmaker

myboard = miniworldmaker.PhysicsBoard()
myboard.size = 400, 300
myboard.add_background((0,0,0,255))
token = miniworldmaker.Token((200,200))
token.size = (40, 40)
token.position = (10, 10)
token.add_costume((200,200,200,200))
myboard.run()
```

Das Token fällt nun automatisch nach unten. Du kannst nun die Eigenschaften des Raums und des Tokens verändern.

---
Diese Beschreibung wird noch fortgesetzt