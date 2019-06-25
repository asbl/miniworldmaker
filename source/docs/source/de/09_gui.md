GUI Elemente
------------

Du kannst an deine Miniwelt verschiedene GUI-Elemente anbieten. 

Einige der GUI-Elemente helfen dir als Designer und Programmierer, andere kannst du als Bedienfläche direkt in deine Miniwelt einbauen.


### Die Toolbar

Die Toolbar ist eine Liste von Schaltflächen.

Eine neue Toolbar initialisierst du so:

```
        toolbar = self.window.add_container(Toolbar(), dock="right")
        toolbar.add_widget(ToolbarButton("Spin"))
```

Folgende Widgets kannst du zur Zeit hinzufügen:

  * ToolbarButton: Ein Button. Beim Klick auf den Button wird das Event Button aufgerufen. 
  Für data wird der Text des Buttons mitgeliefert (Im Beispiel oben z.B. "Spin")
  
  * Ein Label dient dazu Text anzuzeigen.

Siehe auch das Beispiel [spinning_wheel](https://github.com/asbl/miniworldmaker/blob/master/examples/gui/spinning_wheel.py) auf Github.
  
![_images/roboanimation.gif](../_images/spinning_wheel.gif)

### Die Konsole

Die Konsole dient dazu Informationen auszugeben.

Die Konsole wird folgendermaßen initialisiert.

```
        self.console = self._window.add_container(Console(), "bottom")
```

Anschließend kannst du folgendermaßen Ausgaben auf die Konsole schreiben:
```
                self.board.console.print("Du zündest die Feuerstelle an.")
```

### Die Event-Console

Die Event-Leiste ist eine spezielle Console, welche Ereignisse ausgibt, die gesendet werden.
Du kannst die Konsole folgendermaßen initialisieren:

```
        self.window.add_container(event_console, dock="right", size=400)
```

Du wirst feststellen, dass die Ausgabe aber schnell unübersichtlich ist. Daher kannst du entscheiden, auf welche Art von Ereignissen die Konsole reagieren soll.
```
        event_console.register_events = {"key pressed"}
```

Diese Zeile Code bedeutet z.B., dass die Konsole nur auf das Ereigniss key_pressed reagiert. 

### Die Actionbar

Mit der Actionbar kannst du den Programmfluss analysieren, indem du das Programm schrittweise ablaufen lässt.
So initialisierst du die Actionbar:

```
        self.window.add_container(ActionBar(self), dock="bottom")
```

### Die ActiveActorToolbar

Diese Toolbar zeigt dir alle aktuellen Informationen über einen Akteur (Position, Richtung, berührte Ränder, ...) an,

Du kannst die Token-Toolbar folgendermaßen initialisieren:

```
        actor_toolbar = ActiveActorToolbar(self)
        self.window.add_container(actor_toolbar, dock="right", size=400)
```

Der Actor, der mit der Token-Toolbar angezeigt wird, kann durch Klick auf den entsprechenden Actor ausgewählt werden.