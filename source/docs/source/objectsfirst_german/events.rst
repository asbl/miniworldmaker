Ereignisse
**********

Events(Ereignisse) sind ein zentrales Konept des Miniworldmakers:

* Mit Events können Eingaben abgefragt werden (z.B. Mausklicks oder Tastatureingaben).
* Mit Events können Objekte miteinander kommunizieren (z.B. über Nachrichten)

Ein Ereignis registrieren
=========================

Damit das Board oder ein Player auf ein Ereignis reagiert, muss dieses registriert werden.

Dies funktioniert genauso wie bei der `act()`-Methode:

  .. code-block:: python

    @player.register
    def on_key_down_w(self):
        self.move()
 
Hier wird die Methode `on_key_down_w` registriert, die überprüft, ob die Taste w gedrückt wurde.

Sobald die Taste betätigt wird, bewegt sich das Token `player` um einen Schritt nach vorne.

Wie zuvor gilt: Jede registrierte Methode benötigt als ersten Parameter das Schlüsselwort `self` und mit diesem Schlüsselwort kannst du innerhalb der Methode auf Attribute und Methoden des Objekts zugreifen.

on_key_down und on_key_pressed
-------------------------------

Es gibt die beiden Funktionen `on_key_down(self, key)` und `on_key_pressed(self, key)`: 

* Die Funktion `on_key_do```wn` wird genau einmal aufgerufen, wenn die Taste gedrückt wird. 
* Die Taste `on_key_pressed` hingegen wird immer wieder aufgerufen, solange die Taste gedrückt wird. 

Beide Funktionen gibt es sowohl in der Variante `on_key_down_b(self)` / `on_key_pressed_c(self)` um das betätigen einer konkreten Taste abzufragen als auch n der Variante `on_key_down(self, key)`/`on_key_pressed(self, key)` um alle Tastaturabfragen zu verarbeiten.

Nachrichten senden
------------------

Mit `send message(self, message)` kannst du eine globale Nachricht an **alle** Objekte und das Board senden.
Diese Nachrichten können mit `on_message` verarbeitet werden.

Beispiel:

  .. code-block:: python

    @player.register
    def on_message(self, message):
        if message == "Example message":
            do_something()

Ausblick
--------

* `Vollständiges Beispiel <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/05%20-%20events.py>`_
* `Weitere Beispiele <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/05%20-%20events.py>`_
* --> Mehr Informationen. Siehe :doc:`Key Concepts: Events <../key_concepts/events>`.