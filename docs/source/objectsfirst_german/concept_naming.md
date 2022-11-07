# Konzept: Naming und Variablen

## Naming

Im ersten Kapitel hast du Anweisungen der folgenden Art gesehen:

``` python
board = Board()
```

Das `=` Zeichen hat hier eine andere Funktion als in der Mathematik. 

* Zuerst wird die rechte Seite der Anweisung durchgeführt. In diesem Fall wird ein TiledBoard()-Objekt erzeugt.

* Im zweiten Schritt, wird das erzeugte Objekt mit dem Namen `board` gespeichert. Du kannst später über diesen `Namen` immer wieder auf das erzeugte Objekt zugreifen.

Namen haben also in einer Programmiersprache eine ganz besondere Bedeutung, sie dienen dir als ein Speicher für Objekte und Daten. Indem du Objekten einen Namen gibst, kannst du später wieder auf diese zugreifen. Man nennt solche Namen auch **Variablen**, denn das Objekt auf das über den Namen zugegriffen werden kann, kann meist auf verschiedene Arten verändert werden.

Im einfachen Fall kann dies so aussehen:

``` python
a = 3
b = 2
c = a + b
```

Indem du Werte unter dem Namen a und b gespeichert hast, kannst du später wieder darauf zugreifen. In der letzten Zeile wird zuerst `a + b` gerechnet und das Ergebnis in `c` gespeichert. Als Ergebnis wird `5` ausgegeben.

Variablen können jederzeit neue Werte speichern - Der alte Wert geht dabei verloren:

``` python
a = 3
a = 2
c = a + a
print(c)
```

Das Programm gibt `4` aus, da der Wert 3 in der zweiten Zeile überschrieben wird und verloren ist.

## Das Board-Objekt

Das Board ist ein Objekt und bringt verschiedene Attribute und Methoden mit, 
auf die du zugreifen kannst, z.B. `rows`, `columns` und `tile_size`.

### Attribute

Auf Attribute greifst du mit der Syntax `objektname.attributsname` zu.

Beispiel: 

``` python
board.rows = 4
```

Dieser Code speichert den Wert 4 in `board.rows` - Das Board-Objekt hat danach also 4 Zeilen.

### Methoden

Methoden sind Befehle, die ein Objekt ausführen kann, z.B. `board.add_background()` um 
Auf Methoden greifst du mit der Syntax  `objektname.methodenname()`zu. Manchmal stehen in der Klammer noch Variablen

Beispiel:

``` python
board.add_background("images/my_background.png)
```

