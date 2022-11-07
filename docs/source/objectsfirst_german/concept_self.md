# Das Schlüsselwort self

In dem code oben hast du gesehen, dass die Methode ``act`` als Parameter das Schlüsselwort ``self`` erwartet. 

Alle Methoden die zu einem Objekt gehören erhalten dieses Schlüsselwort immer als ersten Paramerer.

Anschließend kann innerhalb der Methode mit diesem Schlüsselwort auf Attribute und Methoden des Objekts selbst zurückgegriffen werden.

Beispiel:

Dieser Code

``` python
@player.register
def act(self):
    self.direction = "right"
```

ist äquivalent zu diesem Code:

``` python
@player.register
def act(self):
    player.direction = "right"
```

`self` bezieht sich hier auf das `player`-Objekt, bei dem die Methode registriert wurde.