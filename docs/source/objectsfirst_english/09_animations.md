# Animations

In the last chapter you were already introduced to animations. Here
different ways how you can create animations: You can use the
you can do:

## Basic animations

If you add multiple images to a costume, you can animate them with

``` python
my_token.costume.add_images(["images/2.png", "images/3.png", "images/4.png"])
# ...
my_token.costume.animate()
```

animate.

With the parameter `loop` you can specify if the animation should be
should be repeated:

``` python
robo.costume.animate(loop = True)
```

## Multiple animations

Often a token needs more than one animation, which can be called
while another animation is still ``running''. This goes for example like this:

``` python
costume_b = robo.add_costume(["images/b1.png", "images/b2.png", "images/b3.png"])
costume_c = robo.add_costume(["images/c1.png", "images/c2.png", "images/c3.png"])

# ...

@player.register
def on_key_pressed_s(self):
    self.animate(costume_b)

@player.register
def on_key_pressed_w(self):
    self.animate(costume_c)
```

## Full example

``` python
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.token((2,6))
player1.add_costume(["images/1.png", "images/2.png", "images/3.png"])
player1.animate()

player2 = miniworldmaker.token((3,6))
player2.add_costume(["images/1.png", "images/2.png", "images/3.png"])
player2.loop_animation(30)

board.run()
```

## Examples
- [More
    Examples](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tests/animations)
