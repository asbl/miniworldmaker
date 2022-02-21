*******************
Training 1
*******************

1. Haus mit Grundformen
#######################

Zeichne ein Haus mit Grundformen:

.. image:: ../_images/processing/house2.png
  :width: 100px
  :alt: House

.. raw:: html

   <details>
   <summary><a>Lösungsansatz</a></summary>

.. code-block:: python

  from miniworldmaker import *

  board = PixelBoard()
  board.size = (120,210)
  Rectangle((10,100), 100, 100)
  Triangle((10,100), (60, 50), (110, 100))

  board.run()

.. raw:: html

   </details>

