from miniworldmaker.boards.data import db_manager


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

class ImportTokensFactory():
    def __init__(self, token_classes):
        self.token_classes = token_classes


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
            "SELECT board_class, width, height, tile_size FROM board")
        self.board.columns = int(data[1])
        self.board.rows = int(data[2])
        self.board.tile_size = int(data[3])
        self.board._loaded_from_db = True
        self.board.switch_board(self.board)
        return self.board


class ImportTokensFromDB(ImportDBFactory, ImportTokensFactory, ImportFactory):
    def __init__(self, file, token_classes):
        ImportDBFactory.__init__(self, file)
        ImportTokensFactory.__init__(self, token_classes)

    def load(self):
        data = self.db.select_all_rows("SELECT token_id, token_class, x, y, direction FROM token")
        if data:
            token_list = []
            for token_data in data:
                class_name = token_data[1]
                x = token_data[2]
                y = token_data[3]
                direction = token_data[4]
                new_token_class_name = class_name
                for token_class in self.token_classes:
                    if token_class.__name__.lower() == new_token_class_name.lower():
                        new_token_class = token_class
                if new_token_class is not None:
                    new_token = new_token_class(position=(x, y))  # Create token
                    new_token.direction = direction
                    token_list.append(new_token)
        return token_list
