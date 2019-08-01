Listen und Schleifen
====================

Listen
------

### Listen erstellen
Eine Liste enthält mehrere Objekte, ohne dass Sie jedem einen neuen Namen geben müssen.

Beispiel:

```
Liste = [0, 1, 2, 2, 3, 4]
```

Die Liste enthält die Zahlen 0-4.

Sie können Listen auch erstellen, indem Sie zuerst eine leere Liste erstellen und dann nacheinander Zahlen hinzufügen:

```
list2 = []
list2.append(5)
list2.append(6)
list2.append(7)
```

Diese Liste enthält die Zahlen 5, 6 und 7.

Ebenso kann eine Liste auch Objekte jeglicher Art enthalten.

```
cliste = []
cliste.append(Circle((40, 40), 60, 0, 0, color=(255, 0, 0, 0, 100))))))
```

Dadurch wird einer Liste ein Kreis hinzugefügt.


### Zugriff auf Listenelemente


Auf die Listenelemente kann mit einem **Index** zugegriffen werden:

```
list2 = []
list2.append(5)
list2.append(6)
list2.append(7)
drucken(list2[0], list2[1])
```

Gibt 5 6 aus, das 0. Listenelement ist 6, das 1. Listenelement ist 6.


Schleifen
---------

Mit Hilfe von Schleifen können Sie Dinge wiederholen. Wenn Sie z.B. 50 Kreise statt 5 erstellen möchten,
der einfachste Weg, dies zu tun, ist mit einer Schleife:

```
Klasse MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255, 255, 255))))
        für i im Bereich (50):
            Circle((random.randint(0,260), random.randint(0,200)), 10, 0, 0, color=(255, 0, 0, 0, 100)))
```

[![](../_images/replit.png)](https://repl.it/@a_siebel/circles)

Das Programm erzeugt 50 Kreise an einer beliebigen Position.

Mit Hilfe von Listen können Sie auch alle Kreise gleichzeitig bewegen.
```
Klasse MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255, 255, 255))))
        self.lst = []
        für i im Bereich (50):
            self.lst.append(Circle((random.randint(0, 800), random.randint(0, 600)), random.randint(10, 20), 0, color=(255, 0, 0, 0, 100))))

    def act(self):
        für Kreis in self.lst:
            circle.y-=random.randint(0,2)
```
[![](../_images/replit.png)](https://repl.it/@a_siebel/circles2)

![](.../_bilder/movingcircles.gif)
