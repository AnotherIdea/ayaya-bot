import os
import sys
import logging


""" GENERAL Configuration """
BOT_USERNAME = os.environ.get("BOT_USERNAME")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")


""" Logger """
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
