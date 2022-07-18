import os
from miniworldmaker.boards.data import db_manager


class ExportFactory():

    def save(self):
        """
        Implemented in concrete factory
        """
        pass


class ExportDBFactory:
    def __init__(self, file):
        self.file = file
        self.db = db_manager.DBManager(file)

    def remove_file(self):
        if os.path.exists(self.file):
            os.remove(self.file)
        self.db = db_manager.DBManager(self.file)

class ExportBoardFactory:
    def __init__(self, board):
        self.board = board


class ExportTokensFactory:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens_serialized = list()
        for token in self.tokens:
            if not (hasattr(token, "export") and token.export == False):
                token_dict = {"x": token.position[0],
                            "y": token.position[1],
                            "direction": token.direction,
                            "token_class": token.__class__.__name__}
                self.tokens_serialized.append(token_dict)


class ExportBoardToDBFactory(ExportFactory, ExportDBFactory, ExportBoardFactory):
    def __init__(self, file, board):
        ExportDBFactory.__init__(self, file)
        ExportBoardFactory.__init__(self, board)

    def save(self):
        query_board = """CREATE TABLE `board` (
                        `board_class`   TEXT,
                        `tile_size`		INTEGER,
                        `height`		INTEGER,
                        `width`		    INTEGER
                        );
                        """
        cur = self.db.cursor
        cur.execute(query_board)
        self.db.commit()
        board_dict = {"board_class": self.board.__class__.__name__,
                      "tile_size": self.board.tile_size,
                      "height": self.board.rows,
                      "width": self.board.columns,                      
                      }
        self.db.insert(table="board", row=board_dict)
        self.db.commit()
        self.db.close_connection()


class ExportTokensToDBFactory(ExportFactory, ExportDBFactory, ExportTokensFactory):
    def __init__(self, file, tokens):
        ExportDBFactory.__init__(self, file)
        ExportTokensFactory.__init__(self, tokens)

    def save(self):
        query_tokens = """     CREATE TABLE `token` (
                        `token_id`		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `x`			    INTEGER,
                        `y`		        INTEGER,
                        `direction`     FLOAT,
                        `token_class`	TEXT
                        );
                        """
        cur = self.db.cursor
        cur.execute(query_tokens)
        self.db.commit()
        for row in self.tokens_serialized:
            self.db.insert(table="token", row=row)
        self.db.commit()
        self.db.close_connection()

