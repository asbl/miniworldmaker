Richtungen
==========

### Winkel

Ein Actor kann sich in verschiedene Richtungen bewegen. Zunächst musst du dazu wissen, wie in Miniworldmaker Winkel interpretiert werden.
Winkel sind unabhängig von der Ausrichtung der Spielfigur:

![movement](/_images/movement.jpg)

  * 0° bedeutet eine Bewegung nach rechts.
  
  * 90° eine Bewegung nach oben (usw).
  
### Winkel als Strings

Einige Winkelgrößen kannst du auch mit Strings bezeichnen:

  * "right": ist äquivalent zu 0°.
  
  * "up" ist äquivalent zu 90°.
  
  * "left" ist äquivalent zu 180°.
  
  * "down" ist äquivalent zu 270°.

Eine spezielle Angabe ist "forward": Im Gegensatz zu den anderen Angaben bedeutet "forward"
 in Blickrichtung der Figur. Im Bild oben entspricht "forward" 0°, da der Akteur nach rechts schaut.

### Methoden und Attribute

#### self.direction

Setzt die Richtung des Akteurs.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: direction
   :noindex:
```

#### self.turn_left

Dreht den Akteur nach links.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: turn_left
   :noindex:
```

#### self.turn_right

Dreht den Akteur nach rechts.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: turn_right
   :noindex:
```

#### self.flip_x

Der Akteur wird über eine zentrale y-Achse gespiegelt.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: flip_x
   :noindex:
```