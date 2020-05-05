from ayaya_bot import AYAYABot
from rule_message_contains import RuleMessageContains
from config import CHANNEL_NAME, BOT_USERNAME, OAUTH_TOKEN, CLIENT_ID


def main():
    rulesList = [RuleMessageContains("ayaya", "sardAYAYA")]
    ayayaBot = AYAYABot(BOT_USERNAME, CHANNEL_NAME, OAUTH_TOKEN, CLIENT_ID, rulesList)
    ayayaBot.run()


if __name__ == "__main__":
    main()
