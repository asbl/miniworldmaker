from collections import defaultdict

class EventManager:
    members = defaultdict()
    class_members = set()

    def __init__(self, token):
        self.token = token
        self.registered_events = defaultdict(set)
        if not EventManager.members:
            EventManager.members[token.__class__] = token.board.event_manager._get_members_for_instance(token)

    @staticmethod
    def get_members(token):
        if token.__class__ in EventManager.members:
            return EventManager.members[token.__class__]
        else:
            EventManager.members[token.__class__] = token.board.event_manager._get_members_for_instance(token)
            return token.board.event_manager._get_members_for_instance(token)

    def self_remove(self):
        """Method is overwritten in subclasses
        """
        pass