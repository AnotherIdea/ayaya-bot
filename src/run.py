import re
import socket
from config import CHANNEL_NAME, BOT_USERNAME, OAUTH_TOKEN, CLIENT_ID

HOST = "irc.chat.twitch.tv"
PORT = 6667


def connect(con):
    con.connect((HOST, PORT))

    send_pass(con, OAUTH_TOKEN)
    send_nick(con, BOT_USERNAME)
    join_channel(con, CHANNEL_NAME)


def send_pong(con, msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(con, chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(con, nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(con, password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(con, chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(con, chan):
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
    print("Connecting to : {}".format(CHANNEL_NAME))
    print("Nickname : {}".format(BOT_USERNAME))
    print("OAUTH_TOKEN : {}".format(OAUTH_TOKEN))
    print("CLIENT_ID : {}".format(CLIENT_ID))
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
            print("Socket died")
            con = socket.socket()
            connect(con)

        except socket.timeout:
            print("Socket timeout")
            con = socket.socket()
            connect(con)


if __name__ == '__main__':
    print("Running !")
    main()
    print("Stopped !")
