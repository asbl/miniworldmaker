import easygui
from easygui.boxes.fileopen_box import fileopenbox


class Ask:
    
    def __init__(self, board):
        self.board = board

    def choices(self, message, choices):
        reply = easygui.buttonbox(message, self.board.title, choices)
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()
        return reply

    def yn(self, message):
        reply = easygui.ynbox(message, self.board.title)
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()
        return reply

    def int(self, message):
        reply = easygui.integerbox(message, self.board.title)
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()
        return reply

    def text(self, message):
        reply = easygui.enterbox(message, self.board.title)
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()
        return reply

    def ok(self, message):
        reply = easygui.buttonbox(message, self.board.title)
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()

    def file(self):
        reply = easygui.fileopenbox()
        # needed for repl.it
        self.board.app.window.add_display_to_repaint_areas()

    def file_save(self):
        reply = easygui.filesavebox()