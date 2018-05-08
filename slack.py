import os
import time
import re
import nsepy
import logging

from logging.config import fileConfig
from slackclient import SlackClient
from slack_utils import get_quotes,get_performance,get_vr_stocks_below
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
    return('\n'.join(response))


funcDict = {
    'quote': get_quotes,
    'p': get_performance,
    'vr': get_vr_stocks_below,
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
        slist = symbol.split();
        if(slist[0] in funcDict.keys()):
            if(symbol == 'help'):
                response = funcDict['help']()
            else:
                response = funcDict[slist[0]](slist[1])
            print(symbol.split());
        else:
            # capitalize the symbol if not
            response = funcDict['quote'](slist[0].upper())


    except Exception as ex:
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

def get_quote_message(symbol):
    try:
        s = nsepy.live.get_quote(symbol)
        #response =  "*{5}*\n_Current quote:_     {0} ({1}%)\n_Day Low:_\t\t     {3}\n_Day High:_\t\t    {2}\n_Open_\t\t\t       {4}".format(s["lastPrice"], s["pChange"],s["dayHigh"],s["dayLow"],s["open"],s["companyName"])
        #response =  "```{5}\nCurrent quote:\t\t{0} ({1}%)\nDay Low:\t\t\t  {3}\nDay High:\t\t\t {2}\nOpen\t\t\t\t  {4}```".format(s["lastPrice"], s["pChange"],s["dayHigh"],s["dayLow"],s["open"],s["companyName"])
        response =  "```{:25}\n{:25}  {:7} ({:5}%)\n{:25}     {:7}\n{:25}    {:7}\n{:25}      {:7}```".format(s["companyName"],"Current quote:",s["lastPrice"],s["pChange"],"Day Low:",s["dayLow"],"Day High:",s["dayHigh"],"Open:",s["open"])
    except Exception:
        response = "Cannot get quote right now. Please try later!"
    return response

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

