Richtungen
==========

### Winkel

Ein Token kann sich in verschiedene Richtungen bewegen. Zunächst musst du dazu wissen, wie in Miniworldmaker Winkel interpretiert werden.
Winkel sind unabhängig von der Ausrichtung der Spielfigur:

![movement](/_images/movement.jpg)

  * 0° bedeutet eine Bewegung nach oben.
  
  * 90° eine Bewegung nach rechts.
  
  * 180° oder - 180° bedeutet eine Bewegung nach unten
  
  * -90° bedeutet eine Bewegung nach links
  
Die Interpretation von Richtungen entsprechen der populären Programmiersprache Scratch, siehe https://en.scratch-wiki.info/wiki/Direction_(value)

Es gibt eine Ausnahme: Die Default-Direction ist in Miniworldmaker 0°, d.h. Tokens zeigen nach oben.
  
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
.. autoclass:: miniworldmaker.tokens.token.Token
   :members: direction
   :noindex:
```

#### self.turn_left

Dreht den Akteur nach links.

```eval_rst
.. autoclass:: miniworldmaker.tokens.token.Token
   :members: turn_left
   :noindex:
```

#### self.turn_right

Dreht den Akteur nach rechts.

```eval_rst
.. autoclass:: miniworldmaker.tokens.token.Token
   :members: turn_right
   :noindex:
```

#### self.flip_x

Der Akteur wird über eine zentrale y-Achse gespiegelt.

```eval_rst
.. autoclass:: miniworldmaker.tokens.token.Token
   :members: flip_x
   :noindex:
```