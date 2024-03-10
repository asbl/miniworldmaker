## Konzept: Framerate


Man kann einstellen, wie oft `act()` aufgerufen wird, indem man die Attribute `board.fps` und `board.speed` konfiguriert.

* `board.fps` definiert die `frame rate`. Analog zu einem Daumenkino, bei dem du mit festgelegter Geschwindigkeit die Seiten umblätterst, 
  definiert die Framerate wie oft pro Sekunde das Bild neu gezeichnet wird.
  `board.fps` hat den Standardwert 60, d.h. es werden 60 Bilder pro Sekunde angezeigt.
  
* Im Attribut `board.frame` wird der aktuelle frame gespeichert. Die Frames seit Programmstart werden hochgezählt.
  
* `board.speed` definiert wie oft die Programmlogik (z.B. act) pro Sekunde aufgerufen wird. 
  Ein Wert von 60 bedeutet, dass die act()-Methode jeden 60. Frame aufgerufen wird.


``` python
  import miniworldmaker as mwm

  board = mwm.Board()
  board.size = (120,210)

  @board.register
  def on_setup(self):
      board.fps = 1
      board.speed = 3
      
  @board.register
  def act(self):
      print(board.frame)

  board.run()
```

Das Programm oben hat die Ausgabe:

```
  3
  6
  9
  12
  15
```

Es wird sehr langsam hochgezählt, weil genau ein Frame pro Sekunde abgespielt wird und jeden 3. Frame
(also alle 3 Sekunden) die Funktion `act()` aufgerufen wird.