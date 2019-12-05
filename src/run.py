import re
import socket
from config import CHANNEL_NAME, BOT_USERNAME, OAUTH_TOKEN, CLIENT_ID
from config import logger

HOST = "irc.chat.twitch.tv"
PORT = 6667


def connect(con):
    con.connect((HOST, PORT))

    send_pass(con, OAUTH_TOKEN)
    send_nick(con, BOT_USERNAME)
    join_channel(con, CHANNEL_NAME)


def send_pong(con, msg):
    logger.debug("Sending PONG {}".format(msg))
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(con, chan, msg):
    logger.debug("Sending PRIVMSG {} :{}".format(chan, msg))
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(con, nick):
    logger.debug("Sending NICK {}".format(nick))
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(con, password):
    logger.debug("Sending PASS {}".format(password))
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(con, chan):
    logger.debug("Sending JOIN {}".format(chan))
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(con, chan):
    logger.debug("Sending PART {}".format(chan))
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(con, msg):
    if "ayaya" in msg.lower():
        send_message(
            con,
            CHANNEL_NAME,
            'sardAYAYA sardAYAYA sardAYAYA sardAYAYA sardAYAYA')


def main():
    logger.info("Connecting to : {}".format(CHANNEL_NAME))
    logger.info("Nickname : {}".format(BOT_USERNAME))
    logger.info("OAUTH_TOKEN : {}".format(OAUTH_TOKEN))
    logger.info("CLIENT_ID : {}".format(CLIENT_ID))
    con = socket.socket()
    connect(con)

    data = ""

    while True:
        try:
            data = data+con.recv(1024).decode('UTF-8')
            data_split = re.split(r"[~\r\n]+", data)
            data = data_split.pop()

            for line in data_split:
                line = str.rstrip(line)
                line = str.split(line)

                if len(line) >= 1:
                    if line[0] == 'PING':
                        send_pong(con, line[1])

                    if line[1] == 'PRIVMSG':
                        message = get_message(line)
                        parse_message(con, message)

        except socket.error:
            logger.error("Socket died")
            con = socket.socket()
            connect(con)

        except socket.timeout:
            logger.warn("Socket timeout")
            con = socket.socket()
            connect(con)


if __name__ == '__main__':
    logger.info("Running !")
    main()
    logger.info("Stopped !")
