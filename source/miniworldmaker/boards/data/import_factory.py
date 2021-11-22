from miniworldmaker.boards.data import db_manager
from miniworldmaker.tokens import token


class ImportFactory():
    def __init__(self):
        pass

    def load(self):
        """
        Implemented in subclasses
        """
        pass


class ImportBoardFactory():
    def __init__(self, board_class):
        self.board_class = board_class
        self.board = self.board_class()


class ImportDBFactory():
    def __init__(self, file):
        self.db = db_manager.DBManager(file)


class ImportBoardFromDB(ImportFactory, ImportDBFactory, ImportBoardFactory):
    def __init__(self, file, board):
        ImportDBFactory.__init__(self, file)
        ImportBoardFactory.__init__(self, board)

    def load(self):
        """
        Loads a sqlite db file.
        """

        data = self.db.select_single_row(
            "SELECT board_class, width, height, tile_size, tile_margin FROM board")
        self.board.switch_board(self.board)
        self.board.columns = int(data[1])
        self.board.rows = int(data[2])
        self.board._tile_size = int(data[3])
        self.board._tile_margin = int(data[4])
        return self.board


class ImportTokensFromDB(ImportDBFactory, ImportFactory):
    def __init__(self, file):
        ImportDBFactory.__init__(self, file)

    def load(self):
        data = self.db.select_all_rows("SELECT token_id, token_class, x, y, direction FROM token")
        if data:
            token_list = []
            for token_data in data:
                class_name = token_data[1]
                x = token_data[2]
                y = token_data[3]
                direction = token_data[4]
                token_class_name = class_name
                token_class = token.Token
                class_list = token.Token.all_subclasses()
                for cls_obj in class_list:
                    if cls_obj.__name__ == token_class_name:
                        token_class = cls_obj
                new_token = token_class(position=(x, y))  # Create token
                new_token.direction = direction
                token_list.append(new_token)
        return token_list
