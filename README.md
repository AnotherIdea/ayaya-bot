# ayaya-bot
Just a Twitch bot which says AYAYA


## Env var
BOT_USERNAME = Your bot username

CHANNEL_NAME = Channel name (must begin by **#**)

OAUTH_TOKEN = See docs twitch (must begin with **oauth:**)

CLIENT_ID = See docs twitch

https://dev.twitch.tv/docs/irc

## Launch the bot
`docker run --restart unless-stopped -d -e BOT_USERNAME='BOT_USERNAME' -e CHANNEL_NAME='#CHANNEL_NAME' -e OAUTH_TOKEN='oauth:OAUTH_TOKEN' -e CLIENT_ID='CLIENT_ID' --name=NAME_FOR_CONTAINER anotheridea/ayaya-bot`

## Stop the bot
`docker stop NAME_FOR_CONTAINER`
