Verzweigungen
==============

Das Luftblasen-Beispiel aus dem letzten Kapitel hat noch einen kleinen Nachteil:

Die Blasen verschwinden irgendwann. Wenn keine Blasen mehr da sind, sitzt man vor einem leeren Fenster.

Hier helfen uns Verzweigungen der Form wenn-dann weiter:

WENN eine Blase den Bildschirmrand erreicht, DANN lösche sie und erstelle eine neue.

Dies kann als Code folgendermaßen aussehen:

```
    def act(self):
        for circle in self.lst:
            circle.y -= (81 - circle.radius) / 10
            if not circle.position.is_on_board():
                self.lst.remove(circle)
                circle.remove()
                self.lst.append(Circle((random.randint(0, 800),
                        random.randint(200, 600)),
                       random.randint(40, 80),
                       0,
                       color=(100, 0, 255, 100),
                       ))
```

Hinweis: Beachte, dass in zwei Zeilen der Kreis gelöscht wird:
```
self.lst.remove(circle)      
```
Diese Anweisung löscht den Kreis aus unserer Liste, so dass nicht mehr auf den Kreis verwiesen wir.d
```
circle.remove()         
```
Dies löscht den Kreis aus dem Speicher.