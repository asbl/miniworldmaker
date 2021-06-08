Animationen 
========

## Animationen

Im letzten Kapitel wurden dir bereits Animationen vorgestellt. Hier werden dir verschiedene Arten vorgestellt, wie du Animationen erzeugen kannst:

### Grundlegende Animationen

Wenn du mehrere Bilder zu einem Kostüm hinzufügst, kannst du diese mit 

```
my_token.costume.add_images(["images/2.png","images/3.png","images/4.png"])
...
my_token.costume.animate()
```

animieren.

Mit dem Parameter `loop`kannst du festlegen, ob die Animation wiederholt werden soll:
```
robo.costume.animate(loop = True)
``` 

### Mehrere Animationen

Oft benötigt ein Token mehrere Animationen, die auch aufgerufen werden können, während eine andere Animation noch "läuft". Dies geht z.B. so:

```
costume_b = robo.add_costume(["images/b1.png","images/b2.png","images/b3.png"])
costume_c = robo.add_costume(["images/c1.png","images/c2.png","images/c3.png"])
...
@player.register
def on_key_pressed_s(self):
    self.animate(costume_b)
@player.register
def on_key_pressed_w(self):
    self.animate(costume_c)
```

### Beispiele

:::{note}  
>➥ Mehr Infos über Richtungen: [Beispiele zu Animationen](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/animations)
:::