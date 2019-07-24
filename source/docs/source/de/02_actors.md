Akteure
=======

### Eine neue Actor-Klasse erstellen

Als nächtes wird ein Akteur auf dem Board platziert.

Dies geht folgendermaßen


```
class Player(Actor):

    def setup(self):
        self.add_image(path="images/char_blue.png")
```

  * Die Zeile 1 erstellt eine neue Klasse als Kindklasse der Klasse Actor.
  
  * In Zeile 3 wird  die setup()-Methode definiert, 
  die beim Erstellen eines neuen Player-Objektes aufgerufen wird.
  
  * In Zeile 4 wird dann zu dem Player-Objekt ein Bild hinzugefügt.

### Den Akteur zum Spielfeld hinzufügen


  Bis jetzt haben wir nur eine Schablone erstellt, um Player-Objekte zu erzeugen.
  Jetzt sollen konkrete Objekte erzeugt und zum Spielfeld hinzugefügt werden.
    Ergänze dazu die setup() - Methode der Spielfeld-Klasse:

```
  player1 = Player(position = (3, 3))
```


