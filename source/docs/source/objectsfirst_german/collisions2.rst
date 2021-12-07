Kollisionen und Sensoren II
****************************

Ein typischer Anwendungsfall ist es herauszufinden, welche Art von **Token** berührt wurde. 

Es gibt für dieses Problem mehrere Lösungen:

Attribut token_type
===================

Du kannst all deinen Objekten ein Objekt ein Attribut `token_type` hinzufügen:

.. code-block:: python

    player2 = miniworldmaker.Token()
    wall = miniworldmaker.Token()
    player2.token_type = "actor"
    wall.token_type = "wall"

    @player1.register
    def on_sensing_token(self, other_token):
        if other_token.token_type == "actor":
            pass # tue etwa
        elif other_token.token_type == "wall":
            pass # tue etwas anders

**Wichtig!**

Bei diesem Zugang musst du **jedem** Objekt ein Attribut `token_type` geben. 
  
Ansonsten musst du auch überprüfen, ob dieses überhaupt vorhanden ist, wenn du nicht möchtest, dass ansonsten dein komplettes Programm abstürzt.

Dies kann man machen mit:
.. code-block:: python

    if  other_token.token_type and other_token.token_type == "actor":

Wenn jedes token über das Attribut `token_type` verfügt, dann kannst du diese Abfrage auch weglassen.
  

Listen
=======

Du kannst Objekte zu einer Liste hinzufügen um zu überprüfen, ob das berührte Objekt in dieser Liste ist.

.. code-block:: python

    walls = []
    player2 = miniworldmaker.Token()
    wall = miniworldmaker.Token()
    walls.append(wall)

    @player1.register
    def on_sensing_token(self, other_token):
        if other_token.token_type in walls:
            pass # tue etwas


**Wichtig!**

Bei diesem Zugang musst du darauf achten, dass gelöschte Objekte auch aus der Liste entfernt werden z.B. auf folgende Art und weise:
.. code-block:: python 

    walls.remove(wall)
    wall.remove()


Klassen
========

Wenn du mit Klassen arbeitest, nimmt dir der **miniworldmaker** etwas Arbeit ab, weil er nun selbst erkennen kann, um welche **Kindklasse** von `Token` es sich bei einem Objekt handelt.

Hier kannst du zu deiner Klasse folgende Methode hinzufügen:

.. code-block::

    def on_sensing_[klassenname](self, other)

Beispiel
--------

.. code-block:: python

    # Die Andere Klasse hat den Namen Torch
    def on_sensing_torch(self, torch):
        print("Sensing torch")
        # ...

Ausblick
========

* `Vollständiges Beispiel <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/07%20-%20sensors_2.py)>`_

