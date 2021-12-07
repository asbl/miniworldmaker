Spielfiguren 
************

Was sind Tokens?
================

Ein **Token** ist ein Spielstein auf deinem Spielbrett. 

Alle Objekte auf deinem Board sind `Tokens`, die auf dem Spielbrett bewegt werden können und die miteinander kommunizieren können.

Beispiel: Ein Token erstellen
-----------------------------

Nachdem du das Spielbrett erstellt hast, wird nun ein `Token`, *(d.h. eine Spielfigur)* auf dem Board platziert. Dies geht so:

.. code-block:: python
    :lineno-start: 1
    :emphasize-lines: 8,9

    import miniworldmaker

    board = miniworldmaker.TiledBoard()
    board.columns = 20
    board.rows = 8
    board.tile_size = 42
    board.add_background("images/soccer_green.jpg")
    player = miniworldmaker.Token()
    player.add_costume("images/player.png")

    board.run()


Was passiert hier?
------------------

* In Zeile 9 wird ein Player-Objekt erstellt.
  
* In Zeile 10 wird dem Player-Objekt ein Küstüm zugewiesen. 

Das Kostüm
==========

Jedes `Board` hat einen `Background`, jedes `Token` hat ein `Costume`. Damit deine Tokens unterschiedlich aussehen, kannst du deinem Token ein Kostüm *anziehen*. 

Beispiel
--------

Die Anweisung dafür lautet:

.. code-block:: python

    token_name.add_costume("path_to_image")


Hinweis: `path_to_image` ist ein (relativer Pfad) zum Bild. 
Du solltest deine Bilder in den Unterordner `images` ablgegen, dann hat das Bild `bild.png` in dem Unterordner `images` den Pfad `images/bild.png`.

Ergebnis
--------

.. image:: /_images/token.jpg
  :width: 100%
  :alt: First Token

FAQ
===

* Mein Token ist **falsch ausgerichtet**, was soll ich tun?
   
  Ein Token ist dann korrekt ausgerichtet, wenn das Bild nach oben guckt. Wenn das Bild per Default in eine andere Richtung ausgerichtet ist, dann hast du zwei Möglichkeiten

* Du kannst das Bild mit einem Bildeditor drehen
* Du kannst in Miniworldmaker die Orientierung des Kostüms ändern. Dies geht mit `my_token.costume.orientation = 90`
  Setze für orientation den passenden Wert, damit das Kostüm korrekt ausgerichtet ist.
* Manchmal ist es auch nötig, einzustellen, dass sich zwar das Token drehen kann, das Kostüm aber immer gleich ausgerichtet sein soll. Dies geht mit `my_token.costume.is_rotatable = False`

Ausblick
========

* --> Mehr Informationen. Siehe :doc:`Key Concepts: Boards <../key_concepts/tokens>` 
* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/1%20Costumes%20and%20Backgrounds>`_