Directions
==========

### Directions in Miniworldmaker

Directions are handled exactly as in the Scratch programming language, 
see [Scratch-Wiki](https://en.scratch-wiki.info/wiki/Direction_(value)).

The default direction is 0°. All tokens are looking "up"

![movement](/_images/movement.jpg)

  * 0° or "up": up
  
  * 90° or "right": Move right
  
  * -90° or "left": Move left
  
  * 180° or "down": Move down
  
  * "forward": Current direction
  
  
### Methods

#### point_in_direction

Sets direction of token:

```{eval-rst}
.. automethod:: miniworldmaker.tokens.token.Token.point_in_direction
   :noindex:
```

#### turn_left

Turns token left by *degrees* degrees

```{eval-rst}
.. automethod:: miniworldmaker.tokens.token.Token.turn_left
   :noindex:
```

#### turn_right

Turns token right by *degrees* degrees

```{eval-rst}
.. automethod:: miniworldmaker.tokens.token.Token.turn_right
   :noindex:
```

#### flip_x

Mirrors Actor over x-Axis

```{eval-rst}
.. automethod:: miniworldmaker.tokens.token.Token.flip_x
   :noindex:
```
  