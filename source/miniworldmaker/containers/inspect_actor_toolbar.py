from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *


class InspectActorToolbar(toolbar.Toolbar):

    def __init__(self):
        super().__init__()
        self.position = "right"
        self.actor = None
        self.register_events.add("all")
        self.register_events.add("debug")
        self.default_size = 280


    def _add_to_window(self, window, dock, size=None):
        super()._add_to_window(window, dock, size)
        for actor in self.window.board.tokens:
          #if self.actor.__class__ == act.Actor:
          self.add_widget(ActorButton(actor=actor, toolbar = self))

    def get_event(self, event, data):
        super().get_event(event, data)
        if event == "active_token":
            self.actor = data
        if self.actor is not None:
            if event == "active_token" or "actor" in event:
                self.actor = data
                self.remove_all_widgets()
                self.add_widget(ToolbarLabel("Class:" + str(self.actor.__class__.__name__)))
                self.add_widget(ToolbarLabel("ID:" + str(self.actor.token_id)))
                self.add_widget(ToolbarLabel("Direction:" + str(self.actor.direction)))
                self.add_widget(ToolbarLabel("position:" + str(self.actor.position)))
                method_list = [func for func in self.actor.__class__.__dict__ if not func.startswith("_") and not func in 'get_event']
                for method in method_list:
                    self.add_widget(MethodButton(text="--> call method: {0}".format(method), actor=self.actor, method = method))
        else:
            for an_actor in self.window.board.tokens:
                if self.actor:
                    self.add_widget(ActorButton(actor=an_actor))


class MethodButton(ToolbarButton):

    def __init__(self, text, actor, method ):
        super().__init__(text=text)
        self.actor = actor
        self.method = method

    def get_event(self, event, data):
        if self.actor is not None:
            getattr(self.actor, str(self.method))()

    def __str__(self):
        return "MethodButton, {0}".format(self.actor)


class ActorButton(ToolbarButton):

    def __init__(self, actor, toolbar):
        super().__init__(text=str(actor.__class__.__name__) + " at " + str(actor.position))
        self.actor = actor
        self._img_path = actor.costume.image_paths[0]
        self.toolbar = toolbar
        self._text_padding = 30

    def get_event(self, event, data):
        if not  self.toolbar.window.board.active_actor == self.actor:
            self.toolbar.window.board.set_active_actor(token = self.actor)
            self.actor.costume.info_overlay = True

    def __str__(self):
        return "ActorButton, {0} at pos: {1}".format(self.actor, self.actor.position)
