#!/bin/sh

pgrep python3.6

if [ $? -eq 1 ]
then
	pkill -9 python3.6
	cd /home/ubuntu/slack_app && /home/ubuntu/slack_app/myvenv/bin/python3.6 /home/ubuntu/slack_app/slack.py > /home/ubuntu/slack_app/slack_log 2>&1 &
fi
