# Fachkonzept: Schleifen

Oft willst du viele Objekte auf einmal erzeugen. Anstatt jeden Befehl immer wieder zu schreiben,
kannst du dafür Schleifen verwenden.

Dieses Beispiel füllt z.B. den kompletten Bildschirm mit ``grass``-Tokens:

```python
for i in range(board.rows):
    for j in range(board.columns):
        g = Token((i, j)))
        g.add_costume("images/grass.png")
        g.static = True
```

`i`und `j` dienen als Zählervariablen und zählen von 0 bis zum Maximalwert hoch.