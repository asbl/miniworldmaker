Aufspüren
==========

Ein Akteur kann aufspüren, ob sich an seiner Position oder vor 
ihm andere Akteure usw. befinden.

Dies geht z.B. mit folgender Funktion:

```
actor.sensing_tokens(distance, token)
```

Die Funktion spürt auf, ob sich an der aktuellen Position des Actors (oder distance Schritte nach vorne) Akteure befinden.
Wenn ja, dann werden diese als Liste zurückgegeben, andernfalls wird None zurückgegeben.

### Beispiel

In dem Beispiel wird überprüft, ob der Akteur vor einer verschlossenen Tür steht:

```
actors_in_front = self.sensing_tokens(distance = 1, token = Door)
        if self.board.door in actors_in_front:
            if self.board.door.closed:
                message = "The Door is closes"
```

### Funktionen zum Aufspüren von Objekten

#### Sensing Tokens

Spürt Tokens auf

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: sensing_tokens
   :noindex:
```

#### Sensing Token

Spürt ein einzelnes Token auf. Die Methode ist effizienter als sensing_tokens

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: sensing_token
   :noindex:
```


#### Sensing Border

Prüft, ob ein Rand in der Nähe ist.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: sensing_borders
   :noindex:
```

#### Sensing Border

Prüft, ob die Position auf dem Spielfeld ist.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: sensing_on_board
   :noindex:
```

#### Sensing Color

Prüft die Farbe unter dem Actor (bezogen auf den Background der Spielwelt)

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: sensing_on_board
   :noindex:
```