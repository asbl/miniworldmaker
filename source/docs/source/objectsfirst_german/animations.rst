Animationen 
***********


Im letzten Kapitel wurden dir bereits Animationen vorgestellt. Hier werden dir verschiedene Arten vorgestellt, wie du Animationen erzeugen kannst:

Grundlegende Animationen
=========================

Wenn du mehrere Bilder zu einem Kostüm hinzufügst, kannst du diese mit 

.. code-block:: python
    
    my_token.costume.add_images(["images/2.png","images/3.png","images/4.png"])
    # ...
    my_token.costume.animate()

animieren.

Mit dem Parameter `loop` kannst du festlegen, ob die Animation wiederholt werden soll:

.. code-block:: python
    
    robo.costume.animate(loop = True)


Mehrere Animationen
===================

Oft benötigt ein Token mehrere Animationen, die auch aufgerufen werden können, während eine andere Animation noch "läuft". Dies geht z.B. so:

.. code-block:: python
    
    costume_b = robo.add_costume(["images/b1.png","images/b2.png","images/b3.png"])
    costume_c = robo.add_costume(["images/c1.png","images/c2.png","images/c3.png"])
    
    # ...
    
    @player.register
    def on_key_pressed_s(self):
        self.animate(costume_b)

    @player.register
    def on_key_pressed_w(self):
    self.animate(costume_c)

Vollständiges Beispiel
======================

.. code-block:: python

    import miniworldmaker

    board = miniworldmaker.TiledBoard()
    board.columns = 20
    board.rows = 8
    board.tile_size = 42
    board.add_background("images/soccer_green.jpg")
    board.speed = 30
    player1 = miniworldmaker.Token((2,6))
    player1.add_costume(["images/1.png", "images/2.png", "images/3.png"])
    player1.animate()

    player2 = miniworldmaker.Token((3,6))
    player2.add_costume(["images/1.png", "images/2.png", "images/3.png"])
    player2.loop_animation(30)

    board.run()


Beispiele
=========

* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/animations>`_
