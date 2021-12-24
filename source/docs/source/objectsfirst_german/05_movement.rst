Bewegung und Ausrichtung 
************************

Mit der ``act()``-Methode kannst du Token in regelmäßigen Abständen ansteuern. Jetzt lernst du, wie du deine Token gezielt in eine Richtung bewegen kannst.


Die move()-Funktion
===================

Die zentrale Funktion zum Bewegen ist die Funktion ``move()``.

Mit der Funktion ``move()`` kannst du dein Objekt um einen oder mehrere Schritte bewegen:


Beispiel
--------

.. code-block:: python

  @player.register
  def act(self):
      self.direction = 90
      self.move()


Das Token **player** schaut nach rechts (90°, siehe :doc:`Key Concepts: Directions <../key_concepts/directions>` ) und bewegt sich dann einen Schritt nach vorne.
Dies wird regelmäßig wiederholt, wenn die Methode act() aufgerufen wird.

move_left, move_right, ...
==========================

Mit der Funktion move() bewegt sich das ``Token`` immer in die aktuelle ``direction``. 

Du kannst das ``Token`` aber auch direkt in eine Richtung bewegen lassen. Dies geht mit den Befehlen ``move_right()``, ``move_left()``, ``move_up()`` und ``m̀ove_down()``.

Beispiel
--------

Dieser Code bewegt das Token in der act()-Methode nach rechts:

.. code-block:: python

  @player.register
  def act(self):
      self.move_right()

move_in_direction
=================

Alternativ kannst du das Token mit ``move_in_direction()`` auch in eine beliebige Richtung bewegen.

Beispiel:
---------

Dies bewegt das Token nach Rechts (Richtung 90°). Siehe :doc:`Key Concepts: Directions <../key_concepts/directions>` um mehr über Richtungen herauszufinden.

.. code-block:: python

  @player.register
  def act(self):
      self.move_in_direction(90)


Das Schlüsselwort self
======================

In dem code oben hast du gesehen, dass die Methode ``act`` als Parameter das Schlüsselwort ``self`` erwartet. Alle Methoden die zu einem Objekt gehören erhalten dieses Schlüsselwort immer als ersten Paramerer.

Anschließend kann innerhalb der Methode mit diesem Schlüsselwort auf Attribute und Methoden des Objekts selbst zurückgegriffen werden.

Beispiel:
---------

``self.direction = 90`` bezieht sich z.B. *auf die eigene* Ausrichtung, ``self.move_in_direction()`` ruft die eigene Methode ``move_in_direction`` auf.

Die Richtung ändern
===================

Die Richtung kannst du mit folgenden Befehlen ändern:

* ``player.turn_left(degrees)`` - Dreht das Token um **degrees** Grad nach links.
* ``player.turn_right(degrees)`` - Dreht das Token um **degrees** Grad nach rechts.
* ``player.direction = degrees``- Gibt dem player-Objekt die absolute Ausrichtung degrees.
  
  Der Wert degrees kann hier entweder als Zahl oder als Text wie in folgender Grafik angegeben werden (0: oben, 180, unten, 90 rechts, -90 links):


  .. image:: /_images/movement.jpg
    :width: 100%
    :alt: Move on board


Ausblick
========

* Mehr Informationen. Siehe :doc:`Key Concepts: Movement <../key_concepts/movement>`.
* Mehr Informationen. Siehe :doc:`Key Concepts: Directions <../key_concepts/directions>`.
* `Vollständiges Beispiel <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/examples/tutorial/04%20-%20movement%20and%20direction.py)>`_
* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/examples/tests/2%20Movement>`_
