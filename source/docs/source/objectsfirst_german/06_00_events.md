# Ereignisse

Events(Ereignisse) sind ein zentrales Konzept des Miniworldmakers:

* Mit Events können Eingaben abgefragt werden (z.B. Mausklicks oder
  Tastatureingaben).
* Mit Events können Objekte miteinander kommunizieren (z.B. über
  Nachrichten)

## Ein Ereignis registrieren

Damit das Board oder ein Player auf ein Ereignis reagiert, muss dieses
registriert werden.

Dies funktioniert genauso wie bei der `act()`-Methode:

``` python
@player.register
def on_key_down_w(self):
    self.move()
```

Hier wird die Methode `on_key_down_w` registriert, die überprüft, ob die
Taste <kbd>w</kbd> gedrückt wurde.

Sobald die Taste betätigt wird, bewegt sich das Token `player` um einen
Schritt nach vorne.

Wie zuvor gilt: Jede registrierte Methode benötigt als ersten Parameter
das Schlüsselwort `self` und mit diesem Schlüsselwort kannst du
innerhalb der Methode auf Attribute und Methoden des Objekts zugreifen.

### on_key_down und on_key_pressed

Es gibt die beiden Funktionen `on_key_down(self, key)` und
`on_key_pressed(self, key)`:

* Die Funktion `on_key_down` wird genau einmal aufgerufen, wenn die
  Taste gedrückt wird.
* Die Funktion `on_key_pressed` hingegen wird immer wieder aufgerufen, 
  solange die Taste gedrückt wird.

```{note}
Beide Funktionen gibt es sowohl in der Variante `on_key_down_b(self)`, 
`on_key_pressed_c(self)` um das betätigen einer konkreten Taste
abzufragen als auch in der Variante `on_key_down(self, key)` 
`on_key_pressed(self, key)` um alle Tastaturabfragen zu verarbeiten.
```

### Beispiel

```python
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_costume("images/player_1.png")
@player.register
def on_key_down_w(self):
    self.move()
@player.register
def on_key_down_a(self):
    self.turn_left()
@player.register
def on_key_down_d(self):
    self.turn_right()
@player.register
def on_key_down_s(self):
    self.move_back()
board.run()
```

### Ausgabe

 <video controls loop width=100%>
  <source src="../_static/token_events.webm" type="video/webm">
  Your browser does not support the video tag.
</video> 


## Nachrichten senden

Mit `send message(self, message)` kannst du eine globale Nachricht an
**alle** Objekte und das Board senden. Diese Nachrichten können mit
`on_message` verarbeitet werden.

Beispiel:

``` python
@player.register
def on_message(self, message):
    if message == "Example message":
        do_something()
```

## Ausblick

* [Vollständiges
    Beispiel](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/05%20-%20events.py)
* [Weitere
    Beispiele](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/05%20-%20events.py)
* Mehr Informationen. Siehe [Key Concepts: Events](../key_concepts/events)
