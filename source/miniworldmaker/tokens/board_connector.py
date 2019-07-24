class BoardConnector():

    def __init__(self, token, board):
        super().__init__()
        self.token = token
        self.board = board

    def remove_from_board(self):
        self.board.tokens.remove(self.token)
        self.token.board = None
