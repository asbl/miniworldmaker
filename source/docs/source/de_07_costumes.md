Kostüme und Hintergrund
========================

### Kostüme

Jeder Aktuer hat ein oder mehrere Kostüme

Ein Kostüm besteht aus einem oder mehreren Bildern und Anweisungen, wie diese Bilder dargestellt werden sollen.

#### Bilder zu einem Kostüm hinzufügen: 

Ein neues Bild zu einem Kostüm hinzufügen:
```
self.add_image("image.jpg")
```

Auf die gleiche Art kannst du auch mehrere Bilder zu einem Kostüm hinzufügen:

```
self.add_image("image1.jpg")
self.add_image("image2.jpg")
```

### Darstellung von Bildern

Folgende Anweisungen ändern die Darstellung von Kostümen:

#### Info Overlay

Zeigt ein Info-Overlay mit Rahmen und Richtung über dem Token


#### is_rotatable

Gibt an, ob das Bild mit der Richtung des Actors mitgedreht wird.


#### is_upscaled

Gibt an, ob das Bild auf die Größe des Tokens hochskaliert werden soll.
Diese Aktion behält das Größenverhältnis zwischen Länge und Breite bei.

#### is_scaled

Gibt an, ob das Bild auf die Größe des Tokens hochskaliert werden soll.
Diese Aktion verändert gegebenenfalls das Größenverhältnis zwischen Länge Breite.



### Mehrere Kostüme anlegen

Du kannst folgendermaßen mehrere Kostüme anlegen:

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



### Der Hintergrund

Das Spielfeld hat einen Hintergrund. Viele Aktionen funktionieren ähnlich wie bei dem Kostüm, allerdings gibt es noch folgende Aktionen, die nur für den Hintergrund Sinn machen:


#### Grid Overlay anzeigen

Zeigt für alle Zellen Ränder an.

#### texture

Neben scale und upscale gibt es für Hintergründe auch die Option, den Hintergrund mit einemm Bild zu "tapezieren"