# slack_app
Slack App for Stock alerts

Steps for deployment:
--------------------

1. Login to AWS
# ssh -i ~/Downloads/key.pem ubuntu@ec2-18-218-38-251.us-east-2.compute.amazonaws.com

Contact Gowtham if you do not have the key.pem

2. Sync the git repo

$ sudo bash
# cd ~/slack_app
# git pull

3. Activate virtual env

# sv

root@ip-172-31-34-93:~# type sv
sv is aliased to `source ~/myvenv/bin/activate'

4. Run the process

# cd ~/slack_app
# nohup python3.6 slack.py &
