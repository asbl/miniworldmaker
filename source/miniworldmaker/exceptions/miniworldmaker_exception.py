from inspect import signature


class MiniworldMakerError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class NoRunError(MiniworldMakerError):
    def __init__(self):
        self.message = "[boardname].run() was not found in your code. This must be the last line in your code \ne.g.:\nboard.run()\n if your board-object is named board."
        super().__init__(self.message)


class MoveInDirectionTypeError(MiniworldMakerError):
    def __init__(self, direction):
        self.message = f"`direction` should be a direction (int, str) or a position (Position, tuple). Found {type(direction)}"
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
        self.message = f'The playing field is too large ({rows} , {columns}) - The size must be specified in tiles, not pixels.\nDid you mean ({int(rows / tile_size)}, {int(rows / tile_size)})?'
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
        self.message = "Costume must not be none"
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


class ColorException(MiniworldMakerError):
    def __init__(self):
        self.message = "color should be a 4-tuple (r, g, b, alpha"
        super().__init__(self.message)


class NoValidBoardPositionError(MiniworldMakerError):
    def __init__(self, value):
        self.message = f"No valid board position, type is {type(value)} and should be a 2-tuple or Position"
        super().__init__(self.message)


class NoValidBoardRectError(MiniworldMakerError):
    def __init__(self, value):
        self.message = f"No valid board rect, type is {type(value)} and should be a 4-tuple or BoardRect"
        super().__init__(self.message)


class CostumeOutOfBoundsError(MiniworldMakerError):
    def __init__(self, token, costume_count, costume_number):
        self.message = f"Token {str(token)} has {costume_count} costumes. You can't access costume #{costume_number}\nRemember: tokens are counted from 0!"
        super().__init__(self.message)


class NoCostumeSetError(MiniworldMakerError):
    def __init__(self, token):
        self.message = f"Token {str(token)} has no costume - You need to setup a costume first."
        super().__init__(self.message)


class SizeOnTiledBoardError(MiniworldMakerError):
    def __init__(self):
        self.message = "You can't set size for tokens on a tiled board (size is always (1,1)"
        super().__init__(self.message)


class TokenArgumentShouldBeTuple(MiniworldMakerError):
    def __init__(self):
        self.message = "First argument to create a Token [position] should be a Tuple. Maybe you forgot brackets?"
        super().__init__(self.message)


class PhysicsSimulationTypeError(MiniworldMakerError):
    def __init__(self):
        self.message = "Physics simulation should be `None`, `static`, `manual` or `simulated`(default)"
        super().__init__(self.message)


class TokenClassNotFound(MiniworldMakerError):
    def __init__(self, name):
        self.message = f"Token class `{name}` not found"
        super().__init__(self.message)


class CantSetAutoFontSize(MiniworldMakerError):
    def __init__(self):
        self.message = "Can't set font-size because auto_font_size is set. Use token.auto_size = False or token.auto_size = 'token'"
        super().__init__(self.message)


class NotImplementedOrRegisteredError(MiniworldMakerError):
    def __init__(self, method):
        self.message = f"Method {method} is not overwritten or registered"


class EllipseWrongArgumentsError(MiniworldMakerError):
    def __init__(self):
        self.message = "Wrong arguments for Ellipse (position: tuple, width: float, height: float"
        super().__init__(self.message)


class RectFirstArgumentError(MiniworldMakerError):
    def __init__(self, start_position):
        self.message = f"Error: First argument `position` of Rectangle should be tuple or Position, value. Found {start_position}, type: {type(start_position)}"
        super().__init__(self.message)


class LineFirstArgumentError(MiniworldMakerError):
    def __init__(self, start_position):
        self.message = f"Error: First argument `start_position` of Line should be tuple , value. Found {start_position}, type: {type(start_position)}"
        super().__init__(self.message)


class LineSecondArgumentError(MiniworldMakerError):
    def __init__(self, end_position):
        self.message = f"Error: Second argument 'end_position' of Line should be tuple, value. Found {end_position}, type: {type(end_position)}"
        super().__init__(self.message)


class NoBoardError(MiniworldMakerError):
    def __init__(self):
        self.message = "Error: Create a board before you place Tokens"
        super().__init__(self.message)


class ImageIndexNotExistsError(MiniworldMakerError):
    def __init__(self, appearance, index):
        self.message = f"Error: Image index {index} does not exist for {appearance}.\n You can't set costume or background -image to a non-existing image"
        super().__init__(self.message)


class TileNotFoundError(MiniworldMakerError):
    def __init__(self, position):
        self.message = f"No valid Tile found for position {position}"
        super().__init__(self.message)


class CornerNotFoundError(MiniworldMakerError):
    def __init__(self, position):
        self.message = f"No valid Corner found for position {position}"
        super().__init__(self.message)


class EdgeNotFoundError(MiniworldMakerError):
    def __init__(self, position):
        self.message = f"No valid Edge found for position {position}"
        super().__init__(self.message)


class RegisterError(MiniworldMakerError):
    def __init__(self, method, instance):
        self.message = f"You can't register {method} to the instance {instance}"
        super().__init__(self.message)


class MissingTokenPartsError(MiniworldMakerError):
    pass


class MissingBoardSensor(MissingTokenPartsError):
    def __init__(self, token):
        self.message = "INTERNAL ERROR: Missing board_sensor"
        del token
        super().__init__(self.message)


class MissingPositionManager(MissingTokenPartsError):
    def __init__(self, token):
        self.message = "INTERNAL ERROR: Missing position_manager"
        del token
        super().__init__(self.message)
