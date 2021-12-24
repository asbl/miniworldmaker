Physik
******

Die Physikengine kannst du mit Hilfe von einem `Physicboard` verwenden: 

In einem Physikboard funktionieren einige Bewegungs- und Kollissionsfunktionen etwas anders als auf anderen Boards:

Erste Schritte
==============

Erstelle zunächst ein Physicsboard und darin ein Token:

.. code-block:: python

  import miniworldmaker

  myboard = miniworldmaker.PhysicsBoard()
  myboard.size = 400, 300
  myboard.add_background((0,0,0,255))
  token = miniworldmaker.Token((200,200))
  token.size = (40, 40)
  token.position = (10, 10)
  token.add_costume((200,200,200,200))
  myboard.run()


Das Token fällt nun automatisch nach unten. Du kannst nun die Eigenschaften des Raums und des Tokens verändern.

Wie soll das Token simuliert werden?
====================================

Es gibt 4 Arten, wie Tokens simuliert werden können:

* "simulated": Die Simulation wird von der Physik-Engine komplett übernommen.
* "manual": Die Physik-Engine ignoriert das Objekt, Kollissionen mit dem Objekt sind aber möglich.
* "static": Wie manual, aber gedacht für Objekte, die sehr selten bewegt werden (z.B. Wände). Wenn du viele Objekte dieser Art erstellst, dann ist die Performance bei Objekten vom Typ "static" höher als bei "manual"
* None: Keine Simulation. Das Objekt wird einfach ignoriert und andere Objekte können sich "durch das Objekt" hindurchbewegen.


*Diese Beschreibung wird noch fortgesetzt*