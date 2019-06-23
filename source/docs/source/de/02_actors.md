Akteure
=======

### Eine neue Actor-Klasse erstellen

Als nächtes wird ein Akteur auf dem Board platziert.

Dies geht folgendermaßen


```
class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")
```

  * Die erste Zeile erstellt eine neue Klasse als Kindklasse der Klasse Actor.
  
  * In der dritten Zeile wird wieder die __init__()-Methode erstellt, 
  die beim Erstellen eines neuen Player-Objektes aufgerufen wird.
  
  * Zeile 4 ruft die init()-Methode der Vaterklasse auf, 
  die zahlreiche Dinge hinter den Kulissen initialisiert.
  
  * In Zeile 5 wird dann zu dem Player-Objekt ein Bild hinzugefügt.

### Den Akteur zum Spielfeld hinzufügen


  Bis jetzt haben wir nur eine Schablone erstellt, um Player-Objekte zu erzeugen.
  Jetzt sollen konkrete Objekte erzeugt und zum Spielfeld hinzugefügt werden.
    Ergänze dazu die __init__() - Methode der Spielfeld-Klasse:

```
  player1 = Player(position = (3, 3)
```


