from rule import Rule
from datetime import datetime


class RuleMessageContains(Rule):
    def __init__(self, contains, _return):
        self.contains = contains
        self._return = _return
        self.lastTime = 0

    def parse_message(self, username, channel, message):
        t = self.lastTime + 300
        now = datetime.timestamp(datetime.now())
        if self.contains in message.lower() and t < now:
            self.lastTime = now
            return self._return
        return None
