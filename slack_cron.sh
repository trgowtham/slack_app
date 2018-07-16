#!/bin/bash

pgrep -af python3.6 | grep slack.py > /dev/null

if [ $? -eq 1 ]
then
        pkill -9 python3.6
        pkill -9 runzeo
        cd /home/ubuntu/slack_app
        source /home/ubuntu/slack_app/myvenv/bin/activate
        python3.6 /home/ubuntu/slack_app/slack.py > /home/ubuntu/slack_app/slack_log 2>&1 &
fi
