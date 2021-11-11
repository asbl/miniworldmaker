from inspect import signature

class MiniworldMakerError(Exception):
    pass


class NoRunError(MiniworldMakerError):
    def __init__(self):
        self.message = "[boardname].run() was not found in your code. This must be the last line in your code \ne.g.:\nboard.run()\n if your board-object is named board."
        super().__init__(self.message)

class BoardInstanceError(MiniworldMakerError):
    def __init__(self):
        self.message = "You can't use class Board - You must use a specific class e.g. PixelBoard, TiledBoard or PhysicsBoard"
        super().__init__(self.message)

class BoardArgumentsError(MiniworldMakerError):
    def __init__(self, columns, rows):
        self.message = f'columns and rows should be int values but types are {type(columns)} and {type(rows)}'
        super().__init__(self.message)


class TiledBoardTooBigError(MiniworldMakerError):
    def __init__(self, columns, rows, tile_size):
        self.message = f'The playing field is too large ({rows} , {columns}) - The size must be specified in tiles, not pixels.\nDid you mean ({int(rows/tile_size)}, {int(rows/tile_size)})?'
        super().__init__(self.message)

class FileNotFoundError(MiniworldMakerError):
    def __init__(self, path):
        self.message = f"File not found. Is your file Path `{path}` correct?" 
        super().__init__(self.message)

class WrongArgumentsError(MiniworldMakerError):
    def __init__(self, method, parameters):
        sig = signature(method)
        self.message = f"Wrong number of arguments for {str(method)}, got {str(parameters)} but should be {str(sig.parameters)}"
        super().__init__(self.message)

class CostumeIsNoneError(MiniworldMakerError):
    def __init__(self):
        self.message = f"Costume must not be none"
        super().__init__(self.message)

class NotCallableError(MiniworldMakerError):
    def __init__(self, method):
        self.message = f"{method} is not a method.."
        super().__init__(self.message)

class NotNullError(MiniworldMakerError):
    def __init__(self, method):
        self.message = f"{method} arguments should not be `None`"
        super().__init__(self.message)                   

class FirstArgumentShouldBeSelfError(MiniworldMakerError):
    def __init__(self, method):
        self.message = f"Error calling {method}. Did you used `self` as first parameter?"
        super().__init__(self.message)       