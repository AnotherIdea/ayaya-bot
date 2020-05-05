import socket
import signal
import sys
from twitch_irc_parser import TwitchIRCParser
from config import logger


class AYAYABot:
    con = None
    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    def __init__(self, botUsername, channelName, oauthToken, clientID, rulesList):
        self.botUsername = botUsername
        self.channelName = channelName
        self.oauthToken = oauthToken
        self.clientID = clientID
        self.parser = TwitchIRCParser()
        self.rulesList = rulesList

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        logger.debug("Initialize {}".format(self))

    def exit_gracefully(self, signum, frame):
        if self.con:
            self.con.close()
            logger.info("Exiting...")
            sys.exit(0)

    def connect_to_channel(self):
        logger.info("Connecting to {}:{}".format(self.HOST, self.PORT))
        self.con = socket.socket()
        self.con.connect((self.HOST, self.PORT))

        self._send_pass()
        self._send_nick()
        self._join_channel()

    def _send_pass(self):
        logger.debug("Sending PASS {}".format(self.oauthToken))
        self.con.send(bytes("PASS {}\r\n".format(self.oauthToken), "UTF-8"))

    def _send_nick(self):
        logger.debug("Sending NICK {}".format(self.botUsername))
        self.con.send(bytes("NICK {}\r\n".format(self.botUsername), "UTF-8"))

    def _join_channel(self):
        logger.debug("Sending JOIN {}".format(self.channelName))
        self.con.send(bytes("JOIN {}\r\n".format(self.channelName), "UTF-8"))

    def _part_channel(self):
        logger.debug("Sending PART {}".format(self.channelName))
        self.con.send(bytes("PART {}\r\n".format(self.channelName), "UTF-8"))

    def _send_pong(self, response):
        logger.debug("Sending PONG {}".format(response))
        self.con.send(bytes("PONG {}\r\n".format(response), "UTF-8"))

    def _data_receive(self):
        return self.con.recv(1024).decode("UTF-8")

    def send_message(self, message):
        logger.debug("Sending PRIVMSG {} {}".format(self.channelName, message))
        self.con.send(
            bytes("PRIVMSG {} {}\r\n".format(self.channelName, message), "UTF-8")
        )

    def parse_message(self, username, channel, message):
        for rule in self.rulesList:
            r = rule.parse_message(username, channel, message)
            if r:
                self.send_message(r)

    def run(self):
        logger.info("Running...")
        self.connect_to_channel()

        while True:
            try:
                data = self._data_receive()
                data = data.rstrip("\r\n")
                logger.debug("data receive : {}".format(repr(data)))

                # we get only the type as we don't know yet if it's a PRIVMSG
                # or a PING message
                parse = self.parser.parse_message(data)
                if parse is None:
                    # log and forget
                    logger.warn("can't parse : {}".format(data))
                else:
                    type, *args = parse
                    if type == "PRIVMSG":
                        username, channel, message = args
                        self.parse_message(username, channel, message)
                    else:  # type == PING
                        message = args
                        self._send_pong(message)

            except socket.error:
                logger.error("Socket died")
                self.con = socket.socket()
                self.connect()

            except socket.timeout:
                logger.warn("Socket timeout")
                self.con = socket.socket()
                self.connect()

    def __repr__(self):
        return "<AYAYABot {} | {}>".format(self.botUsername, self.channelName)
