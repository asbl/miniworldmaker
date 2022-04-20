# Timer

Mit **Timern** kannst du Ereignisse **zeitgesteuert** ausführen. Wenn du
z.B. möchtest dass eine Aktion nicht sofort, sondern mit einigen
Millisekunden oder Sekunden Verzögerung eintritt, dann kannst du einen
Timer verwenden.

:::{note}
Python bietet auch in der library `time` die Funktion `time.sleep(...)`
an.

Diese solltest du allerdings **nicht** benutzen, da die globale
Verzögerung zu Seiteneffekten führen kann.
:::

## Einen Timer starten

Einen Timer kannst du z.B. so starten:

``` python
miniworldmaker.ActionTimer(24, player.move)
```

![UML](/_images/actiontimer.png)

Die Funktion erhält 2 Argumente:

* Nach **24** Frames (1)
* ... wird die Funktion `player.move` ausgeführt (2).

## Die verschiedenen Timer

Es gibt verschiedene Arten von Timer:

### ActionTimer

Der ActionTimer ruft nach einer vorgegebenen Zeit eine Methode mit
Argumenten auf und entfernt sich danach selbst.

``` python
miniworldmaker.ActionTimer(24, player.move, None)
```

Nach 24 Frames wird der Timer aufgerufen und führt dann einmalig die Funktion
`move` des Objekts `player` auf.

### LoopActionTimer

Der LoopActionTimer macht das gleiche wie der Actiontimer, allerdings
wird die Aktion mit gleichen Abständen immer wieder wiederholt. 


So erstellst du einen Loop-Actiontimer:

``` python
loopactiontimer = miniworldmaker.LoopActionTimer(24, player.move)
```

Alle 24 Frames wird die Funktion `move` des Objekts `player` aufgerufen.

So kannst du einen LoopActionTimer wieder entfernen:

``` python
loopactiontimer.unregister()
```

Der Loopactiontimer wird mit diese, Befehl wieder entfernt.

## Timer mit Events abrufen

Ähnlich wie bei den Sensoren kannst du auch für Timer Methoden registrieren, die auf 
ein Timer Event reagieren.

So eine Methode kann z.B. so aussehen:

``` python
@miniworldmaker.timer(frames = 24)
def moving():
    player.move()
``` 

An frame 24 wird die Methode `moving` aufgerufen.

Mit einem Looptimer kann die Funktion so registriert werden:

``` python
@miniworldmaker.loop(frames = 48)
def moving():
    player.turn_left()
    player.move(2)
```

Hier wird die Funktion moving() alle 48 Frames wiederholt.


