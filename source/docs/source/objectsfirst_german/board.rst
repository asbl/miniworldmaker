Das Spielfeld (Board)
*********************

Los geht es!

Die erste Welt
==============

Wir erstellen eine erste Welt. Diese kann mit folgendem Code erzeugt werden:

.. code-block:: python
  :emphasize-lines: 1,3,4,10
  :lineno-start: 1

  import miniworldmaker

  board = miniworldmaker.TiledBoard()
  board.add_background("images/soccer_green.jpg")
  board.columns = 20
  board.rows = 8
  board.tile_size = 42
  board.speed = 30

  board.run()

Was passiert hier?
------------------

* Zeile 1: Die miniworldmaker library wird importiert.
* Zeile 3: Ein neues **Objekt** vom Typ `TiledBoard` wird erzeugt
* Zeile 4: Das neue Objekt erhält einen `background`.
* Zeile 5-8: Es werden verschiedene Attribute von 'board' verändert.
* Zeile 10: Das Spiel wird gestartet. Mit `board.run()` wird eine mainloop gestartet, die das Board immer und immer wieder neu zeichnet. Diese Anweisung **muss** immer die letzte Zeile deines Codes sein.

Ergebnis:
---------

Je nach Hintergrundbild sieht dein Ergebnis so aus:

.. image:: ../_images/first.jpg
  :width: 100%
  :alt: First Miniworldmaker Example


Etwas Theorie: Wie funktioniert der Miniworldmaker?
===================================================

In Miniworldmaker gibt es zwei unterschiedliche Arten von Objekten, die du erzeugen kannst:

* `Board`: Ein Spielbrett auf dem sich Spielfiguren befinden.
  
* `Token`: Spielfiguren die zahlreiche Attribute und Methoden mitbringen, z.B. Bewegung,
    Kollisionsabfrage, ....

In den nächsten Kapiteln lernst du, wie du Tokens erstellen kannst, die miteinander kommunizieren können.

Ausblick: Verschiedene Boards
=============================

Es gibt mehrere Kind-Klassen von Board

* Ein `TiledBoard` ist geeignet für Boards, bei denen sich die Akteure auf "Kacheln" bewegen.
  
* Ein `PixelBoard` ist für pixelgenaue Darstellungen vorgesehen
  
* Ein `PhysicsBoard` simuliert physikalische Eigenschaften und Objekte auf dem Board.
 
  Einige Features der Boards (z.B. Kollisionen) unterscheiden sich geringfügig.

*  Mehr Informationen, siehe :doc:`Key Concepts: Boards <../key_concepts/boards>` 
* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/1%20Costumes%20and%20Backgrounds>`_