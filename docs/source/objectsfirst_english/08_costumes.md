# Costumes

## Tokens and costumes

Each token has one or more costumes. Costumes have
several images with which animations can be described.

![First Token](../_images/costumes.png)

### The first costume

With the function

``` python
self.add_costume("images/image.jpg")
```

you can add a new costume.

If no costume has been added yet, this will automatically be your first costume.
first costume.

## Add more pictures to a costume

With the command **costume.add_image** you can add more images to a costume.
to a costume.

``` python
self.costume.add_image("images/image_2.jpg")
```

Alternatively, you can directly add a list of images to a costume
to a costume:

``` python
self.costume.add_image(["images/image_1.jpg, images/image_2.jpg"])
```

## Animations

2D animations can be thought of as flipbooks. Thereby,
that the image of an actor/token is changed in quick succession,
it looks like the actor is moving.

To do this, you must first add several images to a costume (see
above).

Then you can animate the costume as follows:

``` python
self.costume.is_animated = True
self.costume.animation_speed = 10
```

### Switch between costumes

Here's how to switch between two costumes:

``` python
self.switch_costume()
```

The statement jumps to the next costume. You can also specify as a parameter
a number to jump to a specific costume.
