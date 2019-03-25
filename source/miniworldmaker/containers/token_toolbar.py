from miniworldmaker.containers.toolbar import Toolbar
from miniworldmaker.containers.toolbar_widgets import *


class TokenToolbar(Toolbar):

    def __init__(self, size=100):
        super().__init__(size)
        self.position = "right"
        self.token = None
        self.size = size
        self.label_id = self.add_widget(ToolbarLabel(text="ID"))
        self.label_direction = self.add_widget(ToolbarLabel(text="Direction"))
        self.label_border = self.add_widget(ToolbarLabel(text="Is at Border"))
        self.label_grid = self.add_widget(ToolbarLabel(text="Is on Board"))
        self.colliding = self.add_widget(ToolbarLabel(text="Colliding"))
        self.colliding_actors = self.add_widget(ToolbarLabel(text="colliding_actors"))

    def get_event(self, event, data):
        if event == "active_token":
            self.token = data
        if self.token is not None:
            if event == "active_token" or event == "actor_moved":
                self.token = data
                self.label_id.set_text("ID:" + str(self.token.token_id))
                self.label_direction.set_text("Direction:" + str(self.token.direction))
                self.label_border.set_text("Is at Border:" + str(self.token.is_at_border()))
                self.label_grid.set_text("Is on Board:" + str(self.token.is_on_the_board()))
            if event == "out of grid" and data == self.token:
                self.label_grid.set_text("Is in Grid:" + str(self.token.on_board))
            if event == "border-event" and data == self.token:
                self.label_border.set_text("is at Border:" + str(self.token.borders))
                self.label_border.set_text("Borders:" + str(self.token.touching_borders))
                self.label_direction.set_text("Direction:" + str(self.token.direction))
