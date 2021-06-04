Timer
=====

Mit **Timern** kannst du Ereignisse **zeitgesteuert ausführen. Wenn du z.B. möchtest dass eine Aktion nicht sofort, sondern mit einigen Millisekunden oder Sekunden Verzögerung eintritt, dann kannst du einen Timer verwenden.

::important
Python bietet auch in der library `time` die Funktion `time.sleep(...) an. Diese solltest du allerdings **nicht** benutzen, da die globale Verzögerung zu Seiteneffekten führen kann.
::

## Einen Timer starten

Einen Timer kannst du z.B. so starten:

```
miniworldmaker.ActionTimer(24, player.move)
```

Die Funktion erhält 3 Argumente: *(1)* Nach `24` Frames wird die Funktion *(2)* `player.move` ausgeführt.

### Timer

Es gibt verschiedene Arten von Timer:

#### ActionTimer

Der ActionTimer ruft nach einer vorgegebenen Zeit eine Methode mit Argumenten auf und entfernt sich danach selbst.

```
miniworldmaker.ActionTimer(24, player.move, None)
```

#### LoopActionTimer

Der LoopActionTimer macht das gleiche wie der Actiontimer, allerdings wird die Aktion mit gleichen Abständen immer wieder wiederholt. Wenn diese Schleife enden soll, muss der Timer gelöscht werden:

##### LoopActionTimer erstellen

```
loopactiontimer = miniworldmaker.LoopActionTimer(24, player.move)
```
##### LoopActionTimer löschen

```
loopactiontimer.unregister()
```



