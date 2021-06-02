Kostüme 
========

### Kostüme

Jedes Token verfügt über ein oder mehrere Bilder. 

Indem du das Bild wechselst kannst du z.B. Animationen erschaffen.

![UML Diagramm](../_images/costumes.png)

 > Für Scratch-Umsteiger: Kostüme funktionieren im Miniworldmaker etwas anders als in Scratch.
 > Während in Scratch jedes Kostüm aus genau einem Bild besteht kann ein Kostüm im Miniworldmaker aus mehreren Bildern bestehen.
 > 
 > Auf diese Art kannst du unterschiedliche Posen in einem Kostüm darstellen und unterschiedliche Animationen in unterschiedliche Kostüme auftrennen. 

### Das erste Kostüm

Mit der Funktion
```
self.add_costume("images/image.jpg")
```

kannst du ein neues Kostüm hinzufügen. 

Wenn noch kein Kostüm hinzufefügt wird, wird dies auch automatisch dein erstes Kostüm.


### Weitere Bilder hinzufügen
 
 Mit der Anweisung **costume.add_image** kannst du weitere Bilder zu einem Kostüm hinzufügen. 
 
 ```
self.costume.add_image("images/image_2.jpg")
```

### Ein Kostüm animieren.

Wenn du mehrere Bilder zu einem Kostüm hinzufügen willst, geht dies mit der Option:

### Animationen

2D-Animationen kannst du dir vorstellen wie ein Daumenkino. Dadurch, dass schnell hintereinander das 
Bild eines Akteurs/Token geändert wird, macht es den Anschein, als würde sich der Akteur bewegen.

Dazu musst du zunächst mehrere Bilder zu einem Kostüm hinzufügen (siehe oben).

Anschließend kannst du das Kostüm folgendermaßen animieren:

```
self.costume.is_animated = True
self.costume.animation_speed = 10
```

### Weitere Kostüme hinzufügen.

Mit folgender Anweisung fügst du weitere Kostüme hinzu:

```
my_costume = self.add_costume("image.png")
```

Es wird ein neues Kostüm mit dem Bild image.png angelegt.
Du kannst auch weitere Bilder zu dem Kostüm hinzufügen:

```
my_costume.add_image("image2.png")
```

### Zwischen Kostümen wechseln

Folgendermaßen wechselst du zwischen zwei Kostümen:

```
self.switch_costume()
```

Die Anweisung springt zum nächsten Kostüm. Du kannst als Parameter auch eine Zahl angeben, um zu einem bestimmten Kostüm zu springen.


### Darstellung von Bildern

Es gibt diverse Möglichkeiten das Aussehen deines Bildes anzupassen, z.B. ob dieses rotierbar ist, automatisch skaliert werden soll usw.

--> Hier findest du mehr Infomrationen: [Costumes](../key_concepts/costumes.md)



