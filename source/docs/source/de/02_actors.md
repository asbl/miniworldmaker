Tokens
=======

### Eine neue Token-Klasse erstellen

Als nächtes wird ein Token, d.h. eine Spielfigur auf dem Board platziert.

Dies geht so:

```
class Player(Token):

    def setup(self):
        self.add_image(path="images/char_blue.png")
```

  * In Zeile 1 wird eine neue Klasse als Kindklasse der Klasse Token definiert.
  
  * In Zeile 3 wird  die setup()-Methode definiert, 
  welche beim Erstellen eines neuen Player-Objektes aufgerufen wird.
  
  * In Zeile 4 wird dann zu dem Player-Objekt ein Bild hinzugefügt.

### Das Token zum Spielfeld hinzufügen


  Bis jetzt haben wir nur eine Schablone erstellt, um Player-Objekte zu erzeugen.
  
  Jetzt sollen konkrete Objekte erzeugt und zum Spielfeld hinzugefügt werden.
    Ergänze dazu die setup() - Methode der Board-Klasse, die du zuvor erstellt hast:

```
class MyBoard(TiledBoard):

    def setup(self):
        ...
        player1 = Player(position = (3, 3))
```


