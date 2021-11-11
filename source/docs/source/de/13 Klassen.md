Klassen
======

In der objektorientierten Programmierung unterscheidet man **Objekte** und **Klassen**.

  * Eine **Klasse** ist ein **Bauplan** um damit verschiedene Arten von Objekten erzeugen zu können. Du hast hier bereits Objekte der Klasse `Board` und der Klasse `Token` erzeugt.

  * Objekte werden basierend auf Klassen erzeugt. Alle Objekte teilen sich Attribute und Methoden, die Attributswerte können sich allerdings unterscheiden.

## Eigene Klassen definieren

Indem du eigene Klassen definierst, kannst du neue Baupläne erzeugen mit denen später identische Objekte erzeugt (*Fachbegriff*: **instanziiert**) werden können. Du kannst diese Klasse als **Kindklasse** von bestehenden Klassen entwerfen, damit du das Rad nicht neu erfinden musst. Du kannst auf diese Weise vorhandene Baupläne übernehmen und verändern.

### Ein erstes Beispiel

Ein Token soll mehrere *Lebenspunkte* haben, die bei einer Kollission reduziert werden. Wenn die Lebenspunke auf 0 fallen, wird das Objekt vernichtet.

```{code-block} python
---
lineno-start: 1
---
import miniworldmaker

class PointToken(miniworldmaker.Token):
    def __init__():
        super()
        self.hitpoints = 100
```

Was passiert hier?

  * In Zeile 3 wird eine neue Klasse definiert die von der Klasse `miniworldmaker.Token` *erbt*.

  * In Zeile 4 wird der **Konstruktor** der Klasse definiert. Die Methode __init__() wird dann aufgerufen, wenn ein neues Objekt dieser Klasse instanziiert werden. Im Konstruktor werden alle Eigenschaften der Klasse definiert (hier z.B. hitpoints). Auf diese Eigenschaften kannst du dann später in Methoden zugreifen.

  * In Zeile 5 wird der **Konstruktor** der Elternklasse `miniworldmaker.Token` aufgerufen. Hier werden alle Attribute definiert, die in der Klasse `miniworldmaker.Token` definiert werden (z.B. position, direction, ...). Dies muss immer der erste Aufruf in deinem Konstruktor sein.

  * In Zeile 6 wird das neue Attribut `hitpoints` definiert. Wenn ein neues `PointToken`-Objekt instanziiert wird, wird dieses Attribut mit dem Wert 100 vorbelegt.