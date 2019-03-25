
Animationen
-----------

2D-Animationen kannst du dir vorstellen wie ein Daumenkino. 

Dadurch, dass schnell hintereinander das Bild eines Akteurs/Token geändert wird, macht es den Anschein, als würde sich der Akteur bewegen.

Folgendermaßen kannst du Animationen erstellen:

### 1. Bilder hinzufügen

Füge in der __init__()-Methode einfach mehrere Bilder hinzu:

```
    def __init__(self):
        super().__init__()
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
```


### 2. Animation starten
 
Lege die Geschwindigkeit fest und starte die Animation:
```
    def __init__(self):
        super().__init__()
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
        [...]
        self.animation_speed = 30
        self.is_animated = True
```

Schaue dir dazu auch das Beispiel [roboanimation](https://github.com/asbl/miniworldmaker/blob/master/examples/moving/roboanimation.py) auf github an:

![_images/roboanimation.gif](_images/roboanimation.gif)