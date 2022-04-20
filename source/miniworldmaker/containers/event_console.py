from miniworldmaker.containers import console


class EventConsole(console.Console):
    event_id = 0

    def __init__(self):
        super().__init__()
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.default_size = 600

    def get_event(self, event, data):
        text = "Event {0}: {1}, Data: {2}".format(self.event_id, str(event), str(data))
        self.event_id += 1
        self._text_queue.append(text)
        if len(self._text_queue) > self.lines:
            self._text_queue.pop(0)
        self.dirty = 1
