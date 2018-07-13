import os
import time
import re
import nsepy
import logging
import sys

from logging.config import fileConfig
from slackclient import SlackClient
from slack_utils import get_vr_stocks_alert

token_pre = 'xoxb-356641465604'
#Append the above to the below variable. Masking the token so that it does not get disabled.
token = token_pre + '-CDXc8LeJUx9woOaSrUY5ByCJ'

slack_client = SlackClient(token)

argDict = {
    'market_open': get_vr_stocks_alert,
}

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def slack_message(message, channel):
    # Sends the direct response back to the channel
    slack_client.api_call('chat.postMessage', channel=channel, 
                text=message, username="botuser",
                icon_emoji=':robot_face:')

if __name__ == "__main__":
    fileConfig('logging.ini')
    logger = logging.getLogger()
    arg = sys.argv[1:]
    count = len(arg)
    if count != 1 or arg[0] not in argDict:
        print('Invalid Usage')
        exit()

    response = argDict[arg[0]](-3)
    slack_message(response, 'stock-alerts')

    #print('Sending Message');
    #slack_message("From Python Script", "stocks");

