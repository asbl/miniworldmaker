from collections import defaultdict


class TokenEventManager:
    members = defaultdict()
    class_members = set()

    def __init__(self, token):
        self.token = token
        self.registered_events = defaultdict(set)
        if not TokenEventManager.members:
            TokenEventManager.members[token.__class__] = token.board.event_manager._get_members_for_instance(token)

    @staticmethod
    def get_members(token):
        if token.__class__ in TokenEventManager.members:
            return TokenEventManager.members[token.__class__]
        else:
            TokenEventManager.members[token.__class__] = token.board.event_manager._get_members_for_instance(token)
            return token.board.event_manager._get_members_for_instance(token)

    def self_remove(self):
        """Method is overwritten in subclasses
        """
        pass
