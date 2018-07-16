#!/bin/bash

cd /home/ubuntu/slack_app
source /home/ubuntu/slack_app/myvenv/bin/activate
echo "================================" >> /home/ubuntu/slack_app/slack_alerts.log
echo $1 "Alert" `date` >> /home/ubuntu/slack_app/slack_alerts.log
echo "================================" >> /home/ubuntu/slack_app/slack_alerts.log
python3.6 /home/ubuntu/slack_app/slack_alerts.py $1 >> /home/ubuntu/slack_app/slack_alerts.log 2>&1 &
