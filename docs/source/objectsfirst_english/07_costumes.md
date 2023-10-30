# Costumes and background

Each token has one or more costumes. Costumes have
several images that can be used to describe animations.

The relation between the class `Token` and the class `Costume` can be illustrated as follows
can be illustrated as follows:

``` {mermaid}
classDiagram
    direction LR
    token *-- Costume : contains Costume >

    class Token{
      costumes : list[Costume]
      +add_costume()
      +switch_costume()
      +next_costume()
    }
    class costume{
        int orientation
        bool is_rotatable
        bool is_flipped
        bool is_scaled
        bool is_animated
        ...
        + add_image(path)
        + add_images(list_of_paths)
        + remove_last_image()

    }
```

:::{note}
If you look in the *api* for the attributes and methods of the class `Costume`, you will find them in the class
in the class `Appearance`- This is the parent class of `Costume` and `Background`, because the background of the
the background of the game area and the costumes of the tokens share many attributes.
:::
## The first costume

With the function

``` python
self.add_costume("images/image.jpg")
```

you can add a new costume to a token.

If no costume has been added yet, this will be your first costume.
first costume.

## Add more images to a costume

With the command **costume.add_image** you can add more images to a costume.
to a costume.

``` python
self.costume.add_image("images/image_2.jpg")
```

Alternatively, you can directly add a list of images to a costume
to a costume:

``` python
self.costume.add_images(["images/image_1.jpg, images/image_2.jpg"])
```

## Animations

2D animations can be thought of as flipbooks. Thereby,
that the image of an actor/token is changed in quick succession,
it looks like the actor is moving.

![First Token](../_images/costumes.png)

To do this, you must first add several images to a costume (see
above).

Then you can animate the costume as follows:

``` python
import miniworldmaker as mwm

board = mwm.Board(80,80)

robot = mwm.Token()
robot.size = (80,80)
robot.add_costume("images/drive1.png")
robot.costume.add_image("images/drive2.png")
robot.costume.is_animated = True
robot.costume.loop = True
board.run()
```

 <video controls loop width=300px>
  <source src="../_static/animation1.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### Switch between costumes

Here's how you switch between two costumes:

``` python
self.switch_costume()
```

The statement jumps to the next costume. You can also specify as a parameter
a number to jump to a specific costume.