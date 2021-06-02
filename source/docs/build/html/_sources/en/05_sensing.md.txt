Sensing
==========

Active tracking
-----------------

An actor can track down whether he is at his position or before 
other actors and so on.

This can be done with the following function, for example:

```
actor.sensing_tokens(distance, token)
```

The function detects whether there are actors at the current position of the actor (or distance steps forward).
If so, they are returned as a list, otherwise None is returned.

### Example

The example checks whether the actor is standing in front of a locked door:

```
actors_in_front = self.sensing_tokens(distance = 1, token = door)
        if self.board.door in actors_in_front:
            if self.board.door.closed:
                message = "The Door is closes"
```

Sensing via event methods
-----------------------------

Alternatively, you can also implement event methods: 
The on_sensing_xy method is called every time an actor detects something.

--> see also [events](06_events.md)

### Functions to find objects

#### Sensing Tokens

Tracks tokens

```eval_rst
...autoclass:: miniworldmaker.tokens.token.Token.Token
   :members: sensing_tokens
   :noindex:
```

#### Sensing Token

Tracks a single token. The method is more efficient than sensing_tokens

```eval_rst
...autoclass:: miniworldmaker.tokens.token.Token.Token
   :members: sensing_token
   :noindex:
```


#### Sensing Border

Checks if there's an edge nearby.

```eval_rst
...autoclass:: miniworldmaker.tokens.token.Token.Token
   :members: sensing_borders
   :noindex:
```

#### Sensing Border

Checks if the position is on the playing field.

```eval_rst
...autoclass:: miniworldmaker.tokens.token.Token.Token
   :members: sensing_on_board
   :noindex:
```

#### Sensing Color

Checks the color under the actor (related to the background of the game world)

```eval_rst
...autoclass:: miniworldmaker.tokens.token.Token.Token
   :members: sensing_on_board
   :noindex:
```

Translated with www.DeepL.com/Translator