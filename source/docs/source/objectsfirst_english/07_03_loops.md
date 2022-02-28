# Business concept: Loops

Often you want to create many objects at once. Instead of writing every command over and over again,
you can use loops.

For example, this example fills the entire screen with ``grass`` tokens:

``python
for i in range(board.rows):
    for j in range(board.columns):
        g = token((i, j)))
        g.add_costume("images/grass.png")
        g.static = True
```

`i`and `j` serve as counter variables and count up from 0 to the maximum value.