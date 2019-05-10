Akteure
=======

### Eine neue Actor-Klasse erstellen
Als nächtes wird ein Akteur auf dem Board platziert.

Dies geht prinzipiell ähnlich wie das Erstellen des Spielfeldes:


```
class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")
```

  * Die erste Zeile erstellt eine neue Klasse als Kindklasse der Klasse Actor.
  * In der dritten Zeile wird wieder die __init__()-Methode erstellt, die beim Erstellen eines neuen Player-Objektes aufgerufen wird.
  * Zeile 4 ruft die init()-Methode der Vaterklasse auf, die zahlreiche Dinge hinter den Kulissen initialisiert.
  * In Zeile 5 wird dann zu dem Player-Objekt ein Bild hinzugefügt.

### Den Akteur zum Spielfeld hinzufügen


  Bis jetzt haben wir nur eine Schablone erstellt, um Player-Objekte zu erzeugen.
  Jetzt sollen konkrete Objekte erzeugt und zum Spielfeld hinzugefügt werden.
    Ergänze dazu die __init__() - Methode der Spielfeld-Klasse:

```
    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        player1 = Player( )
        self.add_to_board(player1, position=(3, 3))
```

  * Zeile 3 erstellt das Player Objekt (und ruft die init()-Methode auf.
  * Zeile 4 fügt das erstellte Objekt dem Spielfeld hinzu, damit die Figur nicht im "Niemandsland" lebt.

Zeile 3 und 4 kann man auch kombinieren:

```
  player1 = self.add_actor(Player(), position=(3, 3))
```

### Alternative

Alternativ kann man den Actor auch direkt so erstelen, indem man einen Parameter position hinzufügt und diesen anschließend der Vater-Klasse übergibt.
```
class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image(path="images/char_blue.png")
```

Ein Objekt kann jetzt erstellt werden mit:

```
  player1 = Player(position=(3, 3))
```

### Akteure und Tokens

Akteure sind eine Kindklasse der allgemeienen Klasse Token. Daher können sie auf alle Attribute und Methoden dieser Klasse zugreifen.
Zusätzlich können sie sich aber auch bewegen und haben Sensoren, um ihre Umgebung abzutasten.

Wenn du statische Objekte erstellen willst (Wände, Untergrund, usw.), dann ist es sinnvoller die Klasse Token zu verwenden, da diese Objekte etwas performanter dargestellt werden können.

Das folgende UML-Diagramm zeigt dir, wie die Klassen modelliert sind.

![](../_images/token_uml.png)

