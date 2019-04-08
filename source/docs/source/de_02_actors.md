Akteure
=======

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

Den Akteur zum Spielfeld hinzufügen
-------------------------------------

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