# Kostüme

## Tokens und Kostüme

Jedes Token verfügt über ein oder mehrere Kostüme. Kostüme verfügen über
mehrere Bilder, mit denen Animationen beschrieben werden können.

```{mermaid}
classDiagram
    direction LR
    Token *-- Costume : contains Costume >

    class Token{
      costumes : list[Costume]
      +add_costume()
      +switch_costume()
      +next_costume()
    }
    class Costume{
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

## Das erste Kostüm

Mit der Funktion

``` python
self.add_costume("images/image.jpg")
```

kannst du ein neues Kostüm zu einem Token hinzufügen.

Wenn noch kein Kostüm hinzugefügt wurde, wird dies auch automatisch dein
erstes Kostüm.

## Weitere Bilder zu einem Kostüm hinzufügen

Mit der Anweisung **costume.add_image** kannst du weitere Bilder zu
einem Kostüm hinzufügen.

``` python
self.costume.add_image("images/image_2.jpg")
```

Alternativ kannst du direkt auch eine Liste von Bildern zu einem Kostüm
hinzufügen:

``` python
self.costume.add_images(["images/image_1.jpg, images/image_2.jpg"])
```

## Animationen

2D-Animationen kannst du dir vorstellen wie ein Daumenkino. Dadurch,
dass schnell hintereinander das Bild eines Akteurs/Token geändert wird,
macht es den Anschein, als würde sich der Akteur bewegen.

![First Token](../_images/costumes.png)

Dazu musst du zunächst mehrere Bilder zu einem Kostüm hinzufügen (siehe
oben).

Anschließend kannst du das Kostüm folgendermaßen animieren:

``` python
from miniworldmaker import *

board = Board(80,80)

robot =  Token()
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

### Zwischen Kostümen wechseln

Folgendermaßen wechselst du zwischen zwei Kostümen:

``` python
self.switch_costume()
```

Die Anweisung springt zum nächsten Kostüm. Du kannst als Parameter auch
eine Zahl angeben, um zu einem bestimmten Kostüm zu springen.