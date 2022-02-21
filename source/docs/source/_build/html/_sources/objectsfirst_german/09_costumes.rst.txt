Kostüme 
*******

Tokens und Kostüme
===================

Jedes Token verfügt über ein oder mehrere Kostüme. Kostüme verfügen über mehrere Bilder, mit denen Animationen beschrieben werden können.

.. image:: ../_images/costumes.png
  :width: 100%
  :alt: First Token


Das erste Kostüm
-----------------

Mit der Funktion

.. code-block:: python
  
  self.add_costume("images/image.jpg")


kannst du ein neues Kostüm hinzufügen. 

Wenn noch kein Kostüm hinzugefügt wurde, wird dies auch automatisch dein erstes Kostüm.


Weitere Bilder zu einem Kostüm hinzufügen
=========================================

Mit der Anweisung **costume.add_image** kannst du weitere Bilder zu einem Kostüm hinzufügen. 
 
.. code-block:: python

  self.costume.add_image("images/image_2.jpg")


Alternativ kannst du direkt auch eine Liste von Bildern zu einem Kostüm hinzufügen:

.. code-block:: python

  self.costume.add_image(["images/image_1.jpg, images/image_2.jpg"])



Animationen
===========

2D-Animationen kannst du dir vorstellen wie ein Daumenkino. Dadurch, dass schnell hintereinander das 
Bild eines Akteurs/Token geändert wird, macht es den Anschein, als würde sich der Akteur bewegen.

Dazu musst du zunächst mehrere Bilder zu einem Kostüm hinzufügen (siehe oben).

Anschließend kannst du das Kostüm folgendermaßen animieren:

.. code-block:: python

  self.costume.is_animated = True
  self.costume.animation_speed = 10


Zwischen Kostümen wechseln
--------------------------

Folgendermaßen wechselst du zwischen zwei Kostümen:

.. code-block:: python

  self.switch_costume()


Die Anweisung springt zum nächsten Kostüm. Du kannst als Parameter auch eine Zahl angeben, um zu einem bestimmten Kostüm zu springen.


### Darstellung von Bildern

* Es gibt diverse Möglichkeiten das Aussehen deines Bildes anzupassen, z.B. ob dieses rotierbar ist, automatisch skaliert werden soll usw.
* --> Mehr Informationen. Siehe :doc:`Key Concepts: Costumes <../key_concepts/costumes>`.



