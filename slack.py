import os
import time
import re
import logging

from logging.config import fileConfig
from slackclient import SlackClient
from slack_utils import get_quotes,get_performance,get_vr_stocks_below,get_vr_stocks_live,get_vr_stocks_live_below

token_pre = 'xoxb-356641465604'
#Append the above to the below variable. Masking the token so that it does not get disabled.
token = token_pre + '-CDXc8LeJUx9woOaSrUY5ByCJ'

slack_client = SlackClient(token)
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def help_message():
    response = []
    response.append(f'{"To get current quote: Type ->  symbol":<25}')
    response.append(f'{"To get performance of VR reco: Type ->p symbol":<25}')
    response.append(f'{"To get VR recos under %: Type -> vr %":<25}')
    response.append(f'{"To get Live prices of VR recos : Type -> vrl":<25}')
    response.append(f'{"To get Live prices of VR recos under %: Type -> vrt %":<25}')
    return('\n'.join(response))


funcDict = {
    'quote': get_quotes,
    'p': get_performance,
    'vr': get_vr_stocks_below,
    'vrl': get_vr_stocks_live,
    'vrt': get_vr_stocks_live_below,
    'help': help_message,
}

def slack_message(message, channel):
    # Sends the direct response back to the channel
    slack_client.api_call('chat.postMessage', channel=channel, 
                text=message, username="botuser",
                icon_emoji=':robot_face:')

def slack_direct_message(uname, channel, symbol):
    # Sends the direct response back to the channel
    #response = get_quotes(symbol)
    try:
        print("Sending a slack_direct_message()")
        slist = symbol.split();
        print(slist)
        if(slist[0].lower() in funcDict.keys()):
            if(len(slist) == 1):
                response = funcDict[slist[0].lower()]()
            else:
                response = funcDict[slist[0].lower()](slist[1])
        else:
            # capitalize the symbol if not
            response = funcDict['quote'](slist[0].upper())


    except Exception as ex:
        logging.debug(f'Exception raise: {ex}')
        response = "Invalid value.Exception raised"

    slack_client.api_call(
            "chat.postEphemeral",
            channel=channel,
            text=response, user=uname
    )

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            #print(event["text"],event["user"])
            return event["text"], event["user"], event["channel"]
    return None, None, None

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, filename='slack_stock.log')
    fileConfig('logging.ini')
    logger = logging.getLogger()

    fileHandler = logging.FileHandler('slack_stack.log')
    logger.addHandler(fileHandler)
    #slack_message("Alert!", "stock-alerts");
    if slack_client.rtm_connect(with_team_state=False):
        print("Stock Bot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            symbol, uname, channel = parse_bot_commands(slack_client.rtm_read())
            #print(symbol,uname)
            if uname:
                slack_direct_message(uname, channel, symbol)
               # handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

    #print('Sending Message');
    #slack_message("From Python Script", "stocks");

