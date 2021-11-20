from miniworldmaker.data import import_factory
from miniworldmaker.data import export_factory

class DataBaseHandler():
    def __init__(self, board):
        self.board = board

    def board_from_db(self, file):
        return export_factory.ExportBoardToDBFactory().save()

