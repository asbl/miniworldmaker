Aktives Aufspüren
=================

Zusätzlich zu den Reaktionen auf Ereignisse kann auch aktiv 
der Status des Boards überprüft sowie die Sensoren von Tokens abgefragt werden.

Dies kann z.B. innerhalb einer anderen Ereignismethode passieren, wenn z.B. überprüft werden soll, ob eine Taste gedrückt wurde, während sich zwei Tokens berühren.


Dies geht z.B. mit folgender Funktion:

### Methoden 

  * **player.sensing_tokens(distance, token)**
    
    Spürt Token in Entfernung *distance* auf. Gibt eine Liste von gefundenen Tokens zurück.

  * **player.sensing_tokens(distance, token)**
    
    Spürt Token in Entfernung *distance* auf. Gibt das erste gefundene Token zurück.


### Beispiel

In dem Beispiel wird überprüft, ob der Akteur vor einer verschlossenen Tür steht:

```
actors_in_front = self.sensing_tokens(distance = 1, token = Door)
        if self.board.door in actors_in_front:
            if self.board.door.closed:
                message = "The Door is closes"
```

---> Mehr über Sensoren: [Sensoren](../key_concepts/sensors.md)