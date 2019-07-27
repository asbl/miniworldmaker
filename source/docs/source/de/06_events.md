Ereignisse
===========

Es gibt mehrere wichtige Methoden, die du mit Inhalten füllen kannst:

Spezielle Event-Methoden
-------------------------

### Die act() - Methode

Die Act-Methode wird in kurzen Abständen immer wieder aufrufen. 
Hier kannst du Code platzieren, der immer wieder ausgeführt werden soll, z.B.:
```
    def act(self):
        if not self.look_on_board(direction = "forward"):
            self.turn_left(90)
        self.move()
```

Der Actor schaut ein Feld nach vorne und überprüft, ob dieses noch auf dem Spielfeld liegt. 
Wenn ja, geht er ein Feld vorwärts. Andernfalls dreht er sich um 90° nach links.

### Sensing-Methoden

Jedesmal, wenn ein Akteur etwas anderes aufspürt, werden seine entsprechenden sensing-Methoden aufgerufen:

  * **on_sensing_tokens(token_list)**: Spürt alle Tokens am selben Ort auf.
  * **on_sensing_borders(borders)**: Gibt eine Liste mit Rändern zurück, die zur Zeit berührt werden (z.B. ["right", "top"]
  * **on_sensing_on_board()**: Wird aufgerufen, wenn der Akteur sich auf dem Spielfeld befindet.
  * **on_sensing_not_on_board()**: Wird aufgerufen, wenn sich der Akteur nicht auf dem Spielfeld befindet.
  
Allgemeines Event-Handling mit der get_event-Methode
----------------------------------------------------

### Die get_event(event, data)-Methode

Die get_event(event, data)-Methode) dient dazu, auf Ereignisse verschiedener Art zu reagieren.

  * Der Parameter **event** enthält immer einen String mit dem Ereignis, z.B.:
    * "mouse-left": Es wurde die linke Maustaste gedrückt.
    * ...
    
  * Der Parameter **data** enthält Infos, die zu dem Ereignis passen.
    * "mouse-left", "mouse-right" : Die Kachel im Board auf die geklickt wurde.
    
#### Beispiel:

```
    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.move(direction="up")
            elif "S" in data:
                self.move(direction="down")
            elif "A" in data:
                self.move(direction="left")
            elif "D" in data:
                self.move(direction="right")
```

Der Code überprüft, ob das Ereignis "key_down geworfen wurde.
Im Parameter data wird hier eine Liste mit allen in diesem Moment gedrückten Buttons zurückgegeben.
Es kann daher überprüft werden: **Wenn* der Button X gedrückt wurde, tue ... 