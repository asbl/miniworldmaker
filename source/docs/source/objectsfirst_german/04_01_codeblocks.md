# Konzept: Funktionen und Code-Blöcke

## Funktionen und Decorators

Im letzten Kapitel wurde folgender Code verwendet:

``` python
@board.register
def on_setup(self):
    board.fps = 1
    board.speed = 3
```

* In der zweiten Zeile wird eine Funktion definiert, die bestimmte Anweisungen durchführt (dazu später mehr).

* In der ersten Zeile wird diese Funktion mit einem Decorator versehen. Dieser Decorator "heftet" die Funktion an das Board an. Immer wenn das System die Funktion `board.on_setup` aufrufen will, wird die von dir definierte Funktion aufgerufen.
  Auf diese Weise kannst du später Funktionen definieren, die auf beliebige Ereignisse reagieren, z.B. Tastendrücke, ...

## Einrückung und Code-Blöcke

Die dritte und vierte Zeile des Programmcodes oben sind eingerückt. Dies bedeutet, dass bei Aufruf die beiden eingerückten Zeilen aufgerufen werden.

Code-Blöcke dienen in Python immer dazu, zu definieren wann eine bestimmte Verzweigung in deinem Programm beginnt und wann sie endet. Alles was gleich weit eingerückt wird gehört zu einem gemeinsamen Code-Block.

## Coding-Standards Wie weit sollte eingerückt werden?

Die Programmiersprache Python selbst definiert nicht, wie weit ein Code-Block eingerückt werden soll, ob du drei, vier oder fünf Zeichen verwendest ist egal - Entscheidend ist, dass alle Zeilen *gleich weit* eingerückt sind.

Es gibt in Python aber bestimmte Coding-Standards, auf die sich Programmierer geeinigt haben, damit Code immer ähnlich aussieht.

So hat man sich darauf geeinigt, dass man Code immer 4 Zeichen einrückt. Du kannst dies für dich natürlich anders handhaben - Spätestens wenn ihr im Team arbeitet, ist es aber hilfreich sich an solche Konventionen zu halten.

In Python sind Funktionen und Konventionen in sogenannten PEPs ("Python Enhancement Proposal) definiert. Style Guides findest du z.B. in [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Neben der Einrückung findest du dort noch viel mehr, z.B. schreibt man `a = a + 3` anstatt `a=a+3`, weil ersteres leichter zu lesen ist. die Programmiersprache zwingt dich nicht dazu, aber so ist der Code für andere Programmierer besser zu lesen.

Viele moderne Editoren können dich durch Autoformatierung und Linting darin unterstützen, **sauberen** Code zu schreiben.

