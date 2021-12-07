Timer
*****

Mit **Timern** kannst du Ereignisse **zeitgesteuert** ausführen. Wenn du z.B. möchtest dass eine Aktion nicht sofort, sondern mit einigen Millisekunden oder Sekunden Verzögerung eintritt, dann kannst du einen Timer verwenden.

..  note::
  Python bietet auch in der library `time` die Funktion `time.sleep(...)` an. 

  Diese solltest du allerdings **nicht** benutzen, da die globale Verzögerung zu Seiteneffekten führen kann.

Einen Timer starten
===================

Einen Timer kannst du z.B. so starten:


.. code-block:: python

  miniworldmaker.ActionTimer(24, player.move)

.. image:: /_images/actiontimer.png
  :width: 100%
  :alt: UML


Die Funktion erhält 2 Argumente: 

* Nach `24` Frames (1)
* ... wird die Funktion `player.move` ausgeführt (2).

Die verschiedenen Timer
=======================

Es gibt verschiedene Arten von Timer:

ActionTimer
-----------

Der ActionTimer ruft nach einer vorgegebenen Zeit eine Methode mit Argumenten auf und entfernt sich danach selbst.

.. code-block:: python

  miniworldmaker.ActionTimer(24, player.move, None)


LoopActionTimer
---------------

Der LoopActionTimer macht das gleiche wie der Actiontimer, allerdings wird die Aktion mit gleichen Abständen immer wieder wiederholt. Wenn diese Schleife enden soll, muss der Timer gelöscht werden:

* So erstellst du einen Loop-Actiontimer. Der erste Parameter gibt an in welchen Abständen die Schleife wiederholt werden soll.

  .. code-block:: python

    loopactiontimer = miniworldmaker.LoopActionTimer(24, player.move)

* So kannst du einen LoopActionTimer wieder entfernen.

  .. code-block:: python
    
    loopactiontimer.unregister()



