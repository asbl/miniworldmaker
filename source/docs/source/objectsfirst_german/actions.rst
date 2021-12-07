Die act()-Methode
*****************

Du kannst bis jetzt ein Board erstellen und Tokens darauf gestalten. Diese können sich aber noch nicht bewegen.


Die act()-Methode
-----------------

Das Spielfeld und alle Tokens können über die Methode `act()` gesteuert werden. 
Diese Methode wird immer wieder aufgerufen *(genau genommen: Alle `board.speed` Zeiteinheiten)* bis das Spiel beendet wird.

.. image:: ../_images/act.png
  :width: 100%
  :alt: First Token


Wenn du ein Token erstellst, kannst du mit dem Decorator `@register` eine `act()`-Methode zum Spielfeld oder zu deinen Token hinzufügen:

.. code-block:: python
  :emphasize-lines: 12, 13, 14
  :lineno-start: 1

  import miniworldmaker

  board = miniworldmaker.TiledBoard()
  board.columns = 20
  board.rows = 8
  board.tile_size = 42
  board.add_background("images/soccer_green.jpg")
  board.speed = 30
  player = miniworldmaker.Token()
  player.add_costume("images/player_1.png")
  player.direction = 90
  @player.register
  def act(self):
      self.move()

  board.run()


Was passiert hier?
------------------

* Zeile 12-14: Der Decorator `@player.register` bindet die Methode `act` an das Objekt `player`.

Auf ähnliche Weise wirst du später öfters Reaktionen auf Events bei Objekten registrieren (z.B. Reaktionen auf Tastatur- oder Mauseingaben oder Kollisionsüberprüfungen).

Ausblick
--------

* `Vollständiges Beispiel <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/03%20-%20actions.py>`_
* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/2%20Movement>`_