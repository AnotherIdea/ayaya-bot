import re
from config import logger


class TwitchIRCParser:
    expressionMSG = r"^:(.*)!.*\s(PRIVMSG)\s(#[a-z]*)\s:(.*)$"
    expressionPING = r"^(PING)\s:([a-z\.]*)$"

    def __init__(self):
        self.regexMSG = re.compile(TwitchIRCParser.expressionMSG)
        self.regexPING = re.compile(TwitchIRCParser.expressionPING)
        logger.debug("{} initialized".format(self))

    def is_msg(self, message):
        if self.regexMSG.search(message):
            return True
        return False

    def is_ping(self, message):
        if self.regexPING.search(message):
            return True
        return False

    def parse_message(self, message):
        if self.is_msg(message):
            m = self.regexMSG.search(message)
            # we return group(2) as first because it's our message type PRIVMSG
            return m.group(2), m.group(1), m.group(3), m.group(4)
        elif self.is_ping(message):
            m = self.regexPING.search(message)
            return m.group(1), m.group(2)
        else:
            return None

    def __repr__(self):
        return "<TwitchIRCParser>"
