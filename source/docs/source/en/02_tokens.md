Tokens
=======

A token is a piece on your game board. 

All objects in your Miniworld are tokens that can be moved around the board.

## Create a token

After you have created the game board, a token, *(i.e. a game piece)* is now placed on the board.

This goes like this:

``{code-block} python
---
lineno-start: 1
emphasize-lines: 9,10
---
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.token()
player.add_costume("images/player.png")

board.run()
```

  * In line 9, a player object is created.
  
  * In line 10, a costume is assigned to the player object. 

### The costume

Each `board` has a `background`, each `token` has a `costume`. You **should` assign a costume to a new token. 

The statement for this is usually:
```
token_name.add_costume("path_to_image")
```

![tiles](/_images/add_costume.png)

`path_to_image` is a (relative path) to the image. You should put your images in the subfolder `images`, then the image `image.png` in the subfolder `images` has the path `images/image.png.

### Result

![tiles](/_images/token.jpg)

### View

> --> More information. See [tokens](../key_concepts/tokens.md)


Translated with www.DeepL.com/Translator (free version)