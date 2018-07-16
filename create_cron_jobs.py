from crontab import CronTab

#0,15,30,45 * * * * /home/ubuntu/slack_app/slack_cron.sh # m h  dom mon dow   command
#cd /home/ubuntu/slack_app && /home/ubuntu/slack_app/myvenv/bin/python3.6 /home/ubuntu/slack_app/slack_alerts.py market_open

my_cron = CronTab(user='root')
for job in my_cron:
    if job.comment in ['keep_alive', 'mkt_open_alert', 'mkt_close_alert']:
        print("Deleting", job)
        my_cron.remove(job)
    else:
        print(job)

# Keep-Alive

job = my_cron.new(command='/home/ubuntu/slack_app/slack_keep_alive.sh', comment='keep_alive')
job.minute.every(15)

# Market-Open

job = my_cron.new(command='/home/ubuntu/slack_app/slack_alert_wrapper.sh market_open', comment='mkt_open_alert')
job.minute.on(30)
job.hour.on(9)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')

# Market-Close

job = my_cron.new(command='/home/ubuntu/slack_app/slack_alert_wrapper.sh market_open', comment='mkt_close_alert')
job.minute.on(45)
job.hour.on(15)
job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')

my_cron.write()

print("\n---- Cronjobs active ----\n")

my_cron = CronTab(user='root')
for job in my_cron:
    print(job)
