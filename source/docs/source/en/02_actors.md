Akteure
=======

#### Eine neue Actor-Klasse erstellen

Als nächstes wird ein Akteur auf dem Board platziert.

Dies ist folgendermaßen


```
Klasse Spieler (Schauspieler):

    def setup(self):
        self.add_image(path="images/char_blue.png")
```

  * The Zeile 1 erstellt eine neue Klasse als Kindklasse des Klassenschauspielers.
  
  * In Zeile 3 wird die setup()-Methode definiert, 
  the created a new player objects aufgerufen wird.
  
  * In Zeile 4 wird dann das Player-Objekt ein Bild hinzugefügt.

#### Den Akteur zum Spielfeld hinzufügen


  Bis jetzt haben wir nur ein Schablone erstellt, um Player-Objekte zu erzeugen.
  Jetzt werden konkrete Objekte erzeugt und das Spielfeld hinzugefügt.
    Ergänze to the setup() - Methode the Spielfeld-Klasse:

```
  Spieler1 = Spieler (Position = (3, 3, 3))

Übersetzt mit www.DeepL.com/Translator