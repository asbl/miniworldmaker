from gamegridp import *


class ActorToolbar(Toolbar):

    def __init__(self, size=100):
        super().__init__(size)
        self.position = "right"
        self.actor = None
        self._init_labels()

    def _init_labels(self):
        self.label_id = self.add_widget(ToolbarLabel(text="ID"))
        self.label_direction = self.add_widget(ToolbarLabel(text="Direction"))
        self.label_border = self.add_widget(ToolbarLabel(text="Is at Border"))
        self.label_borders = self.add_widget(ToolbarLabel(text="Borders"))
        self.label_grid = self.add_widget(ToolbarLabel(text="Is in grid"))
        self.colliding = self.add_widget(ToolbarLabel(text="Colliding"))
        self.colliding_actors = self.add_widget(ToolbarLabel(text="colliding_actors"))

    def listen(self, event, data):
        if event == "active_actor":
            print("action-toolbar: active-actor event")
            self.actor = data
            self.label_id.set_text("ID:" + str(self.actor.id))
            self.label_direction.set_text("Direction:"+str(self.actor.direction))
            self.label_border.set_text("Is at Border:" + str(self.actor.is_at_border))
            self.label_grid.set_text("Is in Grid:" + str(self.actor.is_in_grid))
        if event == "out of grid" and data == self.actor:
            self.label_grid.set_text("Is in Grid:" + str(self.actor.is_in_grid))
        if event == "border-event" and data == self.actor:
            print("is_At_border")
            self.label_border.set_text("is at Border:" + str(self.actor.is_at_border))
            self.label_borders.set_text("Borders:" + str(self.actor.touching_borders))
            self.label_direction.set_text("Direction:" + str(self.actor.direction))

    def reset(self):
        super().reset()
        self._init_labels()
