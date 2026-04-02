from crontab import CronTab
from log_cryo_temp import pi_config

# Access the crontab for the current user
cron = CronTab(user=True)

script_path = pi_config['crontab_params']['SCRIPT_PATH']
script_tag = pi_config['crontab_params']['SCRIPT_TAG']

# Create a new job
job = cron.new(command=f'python3 {script_path}', 
               comment=script_tag)

# Set the schedule (Every day at 2:30 AM)
job.minute.every(1)

# Write the job to the real crontab
cron.write()